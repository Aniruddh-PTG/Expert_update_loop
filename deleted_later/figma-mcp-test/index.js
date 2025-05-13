const API_KEY = 'figd_-syLWJla6ZRE2lF_rQK6XUBn9JXC0HBw_dS50av9';
const BASE_URL = 'https://api.figma.com/v1';

// Get user information
async function getUserInfo() {
    try {
        const response = await fetch(`${BASE_URL}/me`, {
            headers: {
                'X-Figma-Token': API_KEY
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('User information:', JSON.stringify(data, null, 2));
        return data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Get file details
async function getFileDetails(fileId) {
    try {
        const response = await fetch(`${BASE_URL}/files/${fileId}`, {
            headers: {
                'X-Figma-Token': API_KEY
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Get file nodes
async function getFileNodes(fileId, nodeIds) {
    try {
        const response = await fetch(`${BASE_URL}/files/${fileId}/nodes?ids=${nodeIds}`, {
            headers: {
                'X-Figma-Token': API_KEY
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('\nNode details:', JSON.stringify(data, null, 2));
        return data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Get image fills from the design
function extractImageFills(node) {
    const images = [];
    
    function traverse(node) {
        if (!node) return;

        // Check if the node has an image fill
        if (node.fills && Array.isArray(node.fills)) {
            node.fills.forEach(fill => {
                if (fill.type === 'IMAGE') {
                    images.push({
                        nodeId: node.id,
                        name: node.name || 'Unnamed Image',
                        type: 'fill',
                        imageRef: fill.imageRef
                    });
                }
            });
        }

        // Check if the node itself is an image
        if (node.type === 'IMAGE') {
            images.push({
                nodeId: node.id,
                name: node.name || 'Unnamed Image',
                type: 'image',
                imageRef: node.imageRef
            });
        }

        // Recursively check children
        if (node.children) {
            node.children.forEach(child => traverse(child));
        }
    }

    traverse(node);
    return images;
}

// Get image URLs
async function getImageUrls(fileId, imageIds) {
    try {
        // Limit the number of images to process at once
        const batchSize = 5;
        const batches = [];
        for (let i = 0; i < imageIds.length; i += batchSize) {
            batches.push(imageIds.slice(i, i + batchSize));
        }

        const results = [];
        for (const batch of batches) {
            console.log(`Processing batch of ${batch.length} images...`);
            const response = await fetch(`${BASE_URL}/images/${fileId}?ids=${batch.join(',')}`, {
                headers: {
                    'X-Figma-Token': API_KEY
                }
            });

            if (!response.ok) {
                console.error(`Error fetching batch: ${response.status} ${response.statusText}`);
                continue;
            }

            const data = await response.json();
            if (data.images) {
                results.push(...Object.entries(data.images).map(([id, url]) => ({ id, url })));
            }

            // Add a small delay between batches to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 500));
        }

        return results;
    } catch (error) {
        console.error('Error fetching image URLs:', error);
        return [];
    }
}

// Extract layout information
function extractLayout(node, depth = 0) {
    const layout = {
        name: node.name,
        type: node.type,
        size: node.absoluteBoundingBox ? {
            width: Math.round(node.absoluteBoundingBox.width),
            height: Math.round(node.absoluteBoundingBox.height)
        } : null,
        children: []
    };

    if (node.children) {
        node.children.forEach(child => {
            layout.children.push(extractLayout(child, depth + 1));
        });
    }

    return layout;
}

// Print layout in a tree structure
function printLayout(layout, depth = 0) {
    const indent = '  '.repeat(depth);
    const size = layout.size ? ` (${layout.size.width}x${layout.size.height})` : '';
    console.log(`${indent}${layout.name} [${layout.type}]${size}`);
    
    layout.children.forEach(child => printLayout(child, depth + 1));
}

// Main function to execute all operations
async function main() {
    try {
        console.log('Getting user information...\n');
        const userInfo = await getUserInfo();
        console.log('User information:', userInfo);
        console.log('\nUser ID:', userInfo.id);
        console.log('Email:', userInfo.email);
        console.log('Handle:', userInfo.handle);

        console.log('\nFetching file details...\n');
        const fileDetails = await getFileDetails('MJLK8uVP8CCOUoaI8gS8pb');
        
        console.log('\nDesign Layout Structure:\n');
        const layout = extractLayout(fileDetails.document);
        printLayout(layout);

        // Find the specific node mentioned in the URL
        const targetNodeId = '400-21739';
        console.log('\nLooking for specific node:', targetNodeId);
        
        // Extract specific node details
        function findNode(node, targetId) {
            if (node.id === targetId) {
                return node;
            }
            if (node.children) {
                for (const child of node.children) {
                    const found = findNode(child, targetId);
                    if (found) return found;
                }
            }
            return null;
        }

        const targetNode = findNode(fileDetails.document, targetNodeId);
        if (targetNode) {
            console.log('\nTarget Node Details:');
            console.log('Name:', targetNode.name);
            console.log('Type:', targetNode.type);
            if (targetNode.absoluteBoundingBox) {
                console.log('Size:', {
                    width: Math.round(targetNode.absoluteBoundingBox.width),
                    height: Math.round(targetNode.absoluteBoundingBox.height)
                });
            }
            console.log('Children:', targetNode.children ? targetNode.children.length : 0);
        } else {
            console.log('Target node not found');
        }

    } catch (error) {
        console.error('Main function error:', error.message);
    }
}

// Run the main function
main(); 