Source config.tape

Type "cat tests/fixtures/links.txt"
Enter
# Taking a look at the file...
Sleep 1000ms
Type "clear"
# Pause for dramatic effect...
Sleep 500ms
Enter
Type "consumo list tests/fixtures/links.txt"
# Pause for dramatic effect...
Sleep 500ms
Enter
Wait /\$/
Sleep 5s

Output list.gif
