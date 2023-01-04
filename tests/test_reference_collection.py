"""For maintainability keep a copy of the reference set tests
separate from the other tests. This will likely change over time and
is important for other implementers.
"""

import pytest

from src.sumfolder1.sumfolders import SumFolders

REFERENCE_DROID_LINUX = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/home/git/sumfolder1/reference/collection/","/home/git/sumfolder1/reference/collection","collection","","Done","","Folder","","2023-01-08T20:53:05","false","","","","","",""
"24","2","file:/home/git/sumfolder1/reference/collection/file_0000","/home/git/sumfolder1/reference/collection/file_0000","file_0000","","Done","10","File","","2023-01-08T18:43:06","false","8cfda2609b880a553759cd6200823f3b","0","","","",""
"25","2","file:/home/git/sumfolder1/reference/collection/file_0001","/home/git/sumfolder1/reference/collection/file_0001","file_0001","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"6","2","file:/home/git/sumfolder1/reference/collection/file_0002","/home/git/sumfolder1/reference/collection/file_0002","file_0002","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"12","2","file:/home/git/sumfolder1/reference/collection/sub_dir_1/","/home/git/sumfolder1/reference/collection/sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-08T20:52:42","false","","","","","",""
"22","12","file:/home/git/sumfolder1/reference/collection/sub_dir_1/file_0003","/home/git/sumfolder1/reference/collection/sub_dir_1/file_0003","file_0003","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"23","12","file:/home/git/sumfolder1/reference/collection/sub_dir_1/file_0004","/home/git/sumfolder1/reference/collection/sub_dir_1/file_0004","file_0004","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"18","12","file:/home/git/sumfolder1/reference/collection/sub_dir_1/file_empty","/home/git/sumfolder1/reference/collection/sub_dir_1/file_empty","file_empty","","Done","0","File","","2018-08-14T18:09:29","false","d41d8cd98f00b204e9800998ecf8427e","0","","","",""
"13","12","file:/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/","/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-08T18:49:00","false","","","","","",""
"21","13","file:/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005","/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005","file_0005","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"20","2","file:/home/git/sumfolder1/reference/collection/sub_dir_2/","/home/git/sumfolder1/reference/collection/sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"9","2","file:/home/git/sumfolder1/reference/collection/sub_dir_3/","/home/git/sumfolder1/reference/collection/sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"10","9","file:/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/","/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"11","10","file:/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"5","2","file:/home/git/sumfolder1/reference/collection/sub_dir_4/","/home/git/sumfolder1/reference/collection/sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-08T18:48:43","false","","","","","",""
"16","5","file:/home/git/sumfolder1/reference/collection/sub_dir_4/file_0006","/home/git/sumfolder1/reference/collection/sub_dir_4/file_0006","file_0006","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"15","5","file:/home/git/sumfolder1/reference/collection/sub_dir_4/file_0007","/home/git/sumfolder1/reference/collection/sub_dir_4/file_0007","file_0007","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"14","5","file:/home/git/sumfolder1/reference/collection/sub_dir_4/file_0008","/home/git/sumfolder1/reference/collection/sub_dir_4/file_0008","file_0008","","Done","10","File","","2023-01-06T00:40:09","false","fdffe4dd2d39c7d9986dbf5c6ec5ad39","0","","","",""
"3","2","file:/home/git/sumfolder1/reference/collection/sub_dir_5/","/home/git/sumfolder1/reference/collection/sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"4","3","file:/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/","/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-08T18:48:24","false","","","","","",""
"7","4","file:/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009","/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009","file_0009","","Done","10","File","","2023-01-08T18:45:46","false","7c1f9f9a4d0ce9a72ee63f37a1b7f694","0","","","",""
"8","4","file:/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010","/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010","file_0010","","Done","10","File","","2023-01-08T18:45:51","false","aececec0bc3f515039aec9e60c413cd3","0","","","",""
"17","2","file:/home/git/sumfolder1/reference/collection/sub_dir_6/","/home/git/sumfolder1/reference/collection/sub_dir_6","sub_dir_6","","Done","","Folder","","2023-01-08T20:53:06","false","","","","","",""
"19","17","file:/home/git/sumfolder1/reference/collection/sub_dir_6/file_empty","/home/git/sumfolder1/reference/collection/sub_dir_6/file_empty","file_empty","","Done","0","File","","2018-08-14T18:09:29","false","d41d8cd98f00b204e9800998ecf8427e","0","","","",""
"""

REFERENCE_DROID_WINDOWS = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/C:/sumfolder1/reference/collection/","C:\\sumfolder1\\reference\\collection","collection","","Done","","Folder","","2023-01-10T13:45:41","false","","","","","",""
"15","2","file:/C:/sumfolder1/reference/collection/file_0000","C:\\sumfolder1\\reference\\collection\\file_0000","file_0000","","Done","10","File","","2023-01-08T18:43:06","false","8cfda2609b880a553759cd6200823f3b","0","","","",""
"16","2","file:/C:/sumfolder1/reference/collection/file_0001","C:\\sumfolder1\\reference\\collection\\file_0001","file_0001","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"14","2","file:/C:/sumfolder1/reference/collection/file_0002","C:\\sumfolder1\\reference\\collection\\file_0002","file_0002","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"3","2","file:/C:/sumfolder1/reference/collection/sub_dir_1/","C:\\sumfolder1\\reference\\collection\\sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-08T20:52:42","false","","","","","",""
"11","3","file:/C:/sumfolder1/reference/collection/sub_dir_1/file_0003","C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_0003","file_0003","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"12","3","file:/C:/sumfolder1/reference/collection/sub_dir_1/file_0004","C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_0004","file_0004","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"10","3","file:/C:/sumfolder1/reference/collection/sub_dir_1/file_empty","C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_empty","file_empty","","Done","0","File","","2018-08-14T18:09:29","false","d41d8cd98f00b204e9800998ecf8427e","0","","","",""
"4","3","file:/C:/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/","C:\\sumfolder1\\reference\\collection\\sub_dir_1\\sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-08T18:49:00","false","","","","","",""
"13","4","file:/C:/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005","C:\\sumfolder1\\reference\\collection\\sub_dir_1\\sub_1_dir_1\\file_0005","file_0005","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"5","2","file:/C:/sumfolder1/reference/collection/sub_dir_2/","C:\\sumfolder1\\reference\\collection\\sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/C:/sumfolder1/reference/collection/sub_dir_3/","C:\\sumfolder1\\reference\\collection\\sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"7","6","file:/C:/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/","C:\\sumfolder1\\reference\\collection\\sub_dir_3\\sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"8","7","file:/C:/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","C:\\sumfolder1\\reference\\collection\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"9","2","file:/C:/sumfolder1/reference/collection/sub_dir_4/","C:\\sumfolder1\\reference\\collection\\sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-08T18:48:43","false","","","","","",""
"17","9","file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0006","C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0006","file_0006","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"18","9","file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0007","C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0007","file_0007","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"19","9","file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0008","C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0008","file_0008","","Done","10","File","","2023-01-06T00:40:09","false","fdffe4dd2d39c7d9986dbf5c6ec5ad39","0","","","",""
"20","2","file:/C:/sumfolder1/reference/collection/sub_dir_5/","C:\\sumfolder1\\reference\\collection\\sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"21","20","file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/","C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-08T18:48:24","false","","","","","",""
"22","21","file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009","C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1\\file_0009","file_0009","","Done","10","File","","2023-01-08T18:45:46","false","7c1f9f9a4d0ce9a72ee63f37a1b7f694","0","","","",""
"23","21","file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010","C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1\\file_0010","file_0010","","Done","10","File","","2023-01-08T18:45:51","false","aececec0bc3f515039aec9e60c413cd3","0","","","",""
"24","2","file:/C:/sumfolder1/reference/collection/sub_dir_6/","C:\\sumfolder1\\reference\\collection\\sub_dir_6","sub_dir_6","","Done","","Folder","","2023-01-08T20:53:06","false","","","","","",""
"25","24","file:/C:/sumfolder1/reference/collection/sub_dir_6/file_empty","C:\\sumfolder1\\reference\\collection\\sub_dir_6\\file_empty","file_empty","","Done","0","File","","2018-08-14T18:09:29","false","d41d8cd98f00b204e9800998ecf8427e","0","","","",""
"""

REFERENCE_SF_LINUX = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file://home/git/sumfolder1/reference/collection,/home/git/sumfolder1/reference/collection,collection,,Done,,Folder,,2023-01-08T20:53:05+01:00,false,,,,,,
2,1,file://home/git/sumfolder1/reference/collection/file_0000,/home/git/sumfolder1/reference/collection/file_0000,file_0000,Text,Done,10,File,,2023-01-08T18:43:06+01:00,TRUE,8cfda2609b880a553759cd6200823f3b,1,x-fmt/111,text/plain,Plain Text File,
3,1,file://home/git/sumfolder1/reference/collection/file_0001,/home/git/sumfolder1/reference/collection/file_0001,file_0001,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,1,file://home/git/sumfolder1/reference/collection/file_0002,/home/git/sumfolder1/reference/collection/file_0002,file_0002,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,1,file://home/git/sumfolder1/reference/collection/sub_dir_1,/home/git/sumfolder1/reference/collection/sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-08T20:52:42+01:00,false,,,,,,
6,5,file://home/git/sumfolder1/reference/collection/sub_dir_1/file_0003,/home/git/sumfolder1/reference/collection/sub_dir_1/file_0003,file_0003,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,5,file://home/git/sumfolder1/reference/collection/sub_dir_1/file_0004,/home/git/sumfolder1/reference/collection/sub_dir_1/file_0004,file_0004,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
8,5,file://home/git/sumfolder1/reference/collection/sub_dir_1/file_empty,/home/git/sumfolder1/reference/collection/sub_dir_1/file_empty,file_empty,,empty source,0,File,,2018-08-14T18:09:29+02:00,FALSE,d41d8cd98f00b204e9800998ecf8427e,0,,,,
9,5,file://home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1,/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-08T18:49:00+01:00,false,,,,,,
10,9,file://home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005,/home/git/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005,file_0005,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
11,1,file://home/git/sumfolder1/reference/collection/sub_dir_2,/home/git/sumfolder1/reference/collection/sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
12,1,file://home/git/sumfolder1/reference/collection/sub_dir_3,/home/git/sumfolder1/reference/collection/sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
13,12,file://home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1,/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
14,13,file://home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2,/home/git/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
15,1,file://home/git/sumfolder1/reference/collection/sub_dir_4,/home/git/sumfolder1/reference/collection/sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-08T18:48:43+01:00,false,,,,,,
16,15,file://home/git/sumfolder1/reference/collection/sub_dir_4/file_0006,/home/git/sumfolder1/reference/collection/sub_dir_4/file_0006,file_0006,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
17,15,file://home/git/sumfolder1/reference/collection/sub_dir_4/file_0007,/home/git/sumfolder1/reference/collection/sub_dir_4/file_0007,file_0007,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
18,15,file://home/git/sumfolder1/reference/collection/sub_dir_4/file_0008,/home/git/sumfolder1/reference/collection/sub_dir_4/file_0008,file_0008,Text,Done,10,File,,2023-01-06T00:40:09+01:00,TRUE,fdffe4dd2d39c7d9986dbf5c6ec5ad39,1,x-fmt/111,text/plain,Plain Text File,
19,1,file://home/git/sumfolder1/reference/collection/sub_dir_5,/home/git/sumfolder1/reference/collection/sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
20,19,file://home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1,/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-08T18:48:24+01:00,false,,,,,,
21,20,file://home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009,/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009,file_0009,Text,Done,10,File,,2023-01-08T18:45:46+01:00,TRUE,7c1f9f9a4d0ce9a72ee63f37a1b7f694,1,x-fmt/111,text/plain,Plain Text File,
22,20,file://home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010,/home/git/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010,file_0010,Text,Done,10,File,,2023-01-08T18:45:51+01:00,TRUE,aececec0bc3f515039aec9e60c413cd3,1,x-fmt/111,text/plain,Plain Text File,
23,1,file://home/git/sumfolder1/reference/collection/sub_dir_6,/home/git/sumfolder1/reference/collection/sub_dir_6,sub_dir_6,,Done,,Folder,,2023-01-08T20:53:06+01:00,false,,,,,,
24,23,file://home/git/sumfolder1/reference/collection/sub_dir_6/file_empty,/home/git/sumfolder1/reference/collection/sub_dir_6/file_empty,file_empty,,empty source,0,File,,2018-08-14T18:09:29+02:00,FALSE,d41d8cd98f00b204e9800998ecf8427e,0,,,,
"""

REFERENCE_SF_WINDOWS = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file:/C:/sumfolder1/reference/collection,C:\\sumfolder1\\reference\\collection,collection,,Done,,Folder,,2023-01-10T13:45:41+01:00,false,,,,,,
2,1,file:/C:/sumfolder1/reference/collection/file_0000,C:\\sumfolder1\\reference\\collection\\file_0000,file_0000,Text,Done,10,File,,2023-01-08T18:43:06+01:00,TRUE,8cfda2609b880a553759cd6200823f3b,1,x-fmt/111,text/plain,Plain Text File,
3,1,file:/C:/sumfolder1/reference/collection/file_0001,C:\\sumfolder1\\reference\\collection\\file_0001,file_0001,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,1,file:/C:/sumfolder1/reference/collection/file_0002,C:\\sumfolder1\\reference\\collection\\file_0002,file_0002,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,1,file:/C:/sumfolder1/reference/collection/sub_dir_1,C:\\sumfolder1\\reference\\collection\\sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-08T20:52:42+01:00,false,,,,,,
6,5,file:/C:/sumfolder1/reference/collection/sub_dir_1/file_0003,C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_0003,file_0003,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,5,file:/C:/sumfolder1/reference/collection/sub_dir_1/file_0004,C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_0004,file_0004,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
8,5,file:/C:/sumfolder1/reference/collection/sub_dir_1/file_empty,C:\\sumfolder1\\reference\\collection\\sub_dir_1\\file_empty,file_empty,,empty source,0,File,,2018-08-14T18:09:29+02:00,FALSE,d41d8cd98f00b204e9800998ecf8427e,0,,,,
9,5,file:/C:/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1,C:\\sumfolder1\\reference\\collection\\sub_dir_1\\sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-08T18:49:00+01:00,false,,,,,,
10,9,file:/C:/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005,C:\\sumfolder1\\reference\\collection\\sub_dir_1\\sub_1_dir_1\\file_0005,file_0005,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
11,1,file:/C:/sumfolder1/reference/collection/sub_dir_2,C:\\sumfolder1\\reference\\collection\\sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
12,1,file:/C:/sumfolder1/reference/collection/sub_dir_3,C:\\sumfolder1\\reference\\collection\\sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
13,12,file:/C:/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1,C:\\sumfolder1\\reference\\collection\\sub_dir_3\\sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
14,13,file:/C:/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2,C:\\sumfolder1\\reference\\collection\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
15,1,file:/C:/sumfolder1/reference/collection/sub_dir_4,C:\\sumfolder1\\reference\\collection\\sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-08T18:48:43+01:00,false,,,,,,
16,15,file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0006,C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0006,file_0006,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
17,15,file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0007,C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0007,file_0007,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
18,15,file:/C:/sumfolder1/reference/collection/sub_dir_4/file_0008,C:\\sumfolder1\\reference\\collection\\sub_dir_4\\file_0008,file_0008,Text,Done,10,File,,2023-01-06T00:40:09+01:00,TRUE,fdffe4dd2d39c7d9986dbf5c6ec5ad39,1,x-fmt/111,text/plain,Plain Text File,
19,1,file:/C:/sumfolder1/reference/collection/sub_dir_5,C:\\sumfolder1\\reference\\collection\\sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
20,19,file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1,C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-08T18:48:24+01:00,false,,,,,,
21,20,file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009,C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1\\file_0009,file_0009,Text,Done,10,File,,2023-01-08T18:45:46+01:00,TRUE,7c1f9f9a4d0ce9a72ee63f37a1b7f694,1,x-fmt/111,text/plain,Plain Text File,
22,20,file:/C:/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010,C:\\sumfolder1\\reference\\collection\\sub_dir_5\\sub_5_dir_1\\file_0010,file_0010,Text,Done,10,File,,2023-01-08T18:45:51+01:00,TRUE,aececec0bc3f515039aec9e60c413cd3,1,x-fmt/111,text/plain,Plain Text File,
23,1,file:/C:/sumfolder1/reference/collection/sub_dir_6,C:\\sumfolder1\\reference\\collection\\sub_dir_6,sub_dir_6,,Done,,Folder,,2023-01-08T20:53:06+01:00,false,,,,,,
24,23,file:/C:/sumfolder1/reference/collection/sub_dir_6/file_empty,C:\\sumfolder1\\reference\\collection\\sub_dir_6\\file_empty,file_empty,,empty source,0,File,,2018-08-14T18:09:29+02:00,FALSE,d41d8cd98f00b204e9800998ecf8427e,0,,,,
"""


@pytest.mark.parametrize(
    "droid_report",
    [
        (REFERENCE_DROID_LINUX),
        (REFERENCE_DROID_WINDOWS),
        (REFERENCE_SF_LINUX),
        (REFERENCE_SF_WINDOWS),
    ],
)
def test_alphanumeric_ordering(tmp_path, droid_report):
    """Ensure that directory names are in alphabetical order."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    root_hash = "52b94608dc70813aa88dae01176dc73b"
    assert folder_sum.folders[0].hash_ == root_hash

    folders = folder_sum.folders
    files = folder_sum.files

    match = "d41d8cd98f00b204e9800998ecf8427e"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "File"

    assert len(res["query"]["results"]) == 2

    assert res["query"]["results"][0]["containing_dirs"] == [
        "82301616d7e24f474dbe21de93af0a34",
        "52b94608dc70813aa88dae01176dc73b",
    ]
    assert res["query"]["results"][1]["containing_dirs"] == [
        "74be16979710d4c4e7c6647856088456",
        "52b94608dc70813aa88dae01176dc73b",
    ]
