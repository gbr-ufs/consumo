Source config.tape

Type "echo 'https://example.com' > links.txt"
Sleep 500ms
Enter
Type "echo 'https://example.org' >> links.txt"
Sleep 500ms
Enter
Type "consumo list links.txt"
Sleep 500ms
Enter
Wait /\$/
Sleep 5s

Output list.gif
