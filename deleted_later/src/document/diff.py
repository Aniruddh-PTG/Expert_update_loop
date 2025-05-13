from typing import List, Dict, Tuple
import difflib
from dataclasses import dataclass

@dataclass
class Change:
    section: str
    old_text: str
    new_text: str
    change_type: str  # 'addition', 'deletion', 'modification'

class DocumentDiffer:
    @staticmethod
    def compare_documents(old_sections: Dict[str, str], new_sections: Dict[str, str]) -> List[Change]:
        """
        Compare two versions of a document and return a list of changes
        """
        changes = []
        
        # Compare sections that exist in both documents
        common_sections = set(old_sections.keys()) & set(new_sections.keys())
        for section in common_sections:
            if old_sections[section] != new_sections[section]:
                changes.append(Change(
                    section=section,
                    old_text=old_sections[section],
                    new_text=new_sections[section],
                    change_type='modification'
                ))
        
        # Find sections that were added
        for section in set(new_sections.keys()) - set(old_sections.keys()):
            changes.append(Change(
                section=section,
                old_text="",
                new_text=new_sections[section],
                change_type='addition'
            ))
        
        # Find sections that were removed
        for section in set(old_sections.keys()) - set(new_sections.keys()):
            changes.append(Change(
                section=section,
                old_text=old_sections[section],
                new_text="",
                change_type='deletion'
            ))
        
        return changes
    
    @staticmethod
    def get_line_diff(old_text: str, new_text: str) -> List[Tuple[str, str]]:
        """
        Get a line-by-line diff between two text blocks
        Returns list of (line_type, line_content) tuples
        """
        diff = difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            lineterm=''
        )
        
        result = []
        for line in diff:
            if line.startswith('+'):
                result.append(('addition', line[1:]))
            elif line.startswith('-'):
                result.append(('deletion', line[1:]))
            elif line.startswith(' '):
                result.append(('context', line[1:]))
                
        return result 