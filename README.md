# Documentation

# Налаштування
mysql -D abills < Documentation.sql

ln -s /usr/abills/Abills/modules/Documentation/doc.cgi /usr/abills/cgi-bin/doc.cgi

https://192.168.1.200:9443/doc.cgi?url=abills

Прописати в config.pl настпуний параметр щоб відбувався редірект на нову документацію: 
- $conf{NEW_WIKI} = 1;
