f=open('gutenberg_edited.txt', 'r', encoding="utf8")
final=open('gutenberg_1m.txt', 'w', encoding="utf8")
i=0
for line in f:
  i=i+1
  final.write(line)
  if i>1007155:
    break
  
final.close()