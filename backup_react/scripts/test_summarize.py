import requests

files = {
    'original': open('testlead_files/Password_Test_Cases.docx', 'rb'),
    'modified': open('modified_files/Password_Test_Cases modified.docx', 'rb')
}
response = requests.post('http://localhost:5000/summarize-docx', files=files)
print(response.json()) 