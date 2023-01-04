"""Test merkle/radix tree functionality."""

import hashlib

import pytest

from src.sumfolder1.storageobjects import Folder
from src.sumfolder1.sumfolders import SumFolders

DROID_LINUX_CSV = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/archive/","/archive","archive","","Done","","Folder","","2023-01-04T23:28:05","false","","","","","",""
"9","2","file:/archive/sub_dir_1/","/archive/sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-04T23:29:44","false","","","","","",""
"18","9","file:/archive/sub_dir_1/file_1","/archive/sub_dir_1/file_1","file_1","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"15","9","file:/archive/sub_dir_1/file_2","/archive/sub_dir_1/file_2","file_2","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"10","9","file:/archive/sub_dir_1/sub_1_dir_1/","/archive/sub_dir_1/sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-04T23:29:54","false","","","","","",""
"12","10","file:/archive/sub_dir_1/sub_1_dir_1/file_3","/archive/sub_dir_1/sub_1_dir_1/file_3","file_3","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"11","2","file:/archive/sub_dir_2/","/archive/sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/archive/sub_dir_3/","/archive/sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"7","6","file:/archive/sub_dir_3/sub_3_empty_1/","/archive/sub_dir_3/sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"8","7","file:/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"5","2","file:/archive/sub_dir_4/","/archive/sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-04T23:30:30","false","","","","","",""
"16","5","file:/archive/sub_dir_4/file_4","/archive/sub_dir_4/file_4","file_4","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"14","5","file:/archive/sub_dir_4/file_5","/archive/sub_dir_4/file_5","file_5","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"17","5","file:/archive/sub_dir_4/file_6","/archive/sub_dir_4/file_6","file_6","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"3","2","file:/archive/sub_dir_5/","/archive/sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"4","3","file:/archive/sub_dir_5/sub_5_dir_1/","/archive/sub_dir_5/sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-04T23:31:00","false","","","","","",""
"13","4","file:/archive/sub_dir_5/sub_5_dir_1/file_7","/archive/sub_dir_5/sub_5_dir_1/file_7","file_7","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"""

DROID_WINDOWS_CSV = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/C:/Users/droid_user/sumfolder1/reference/archive/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive","archive","","Done","","Folder","","2023-01-05T10:27:00","false","","","","","",""
"3","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-04T23:29:44","false","","","","","",""
"8","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_1","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_1","file_1","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"9","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_2","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_2","file_2","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"4","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-04T23:29:54","false","","","","","",""
"7","4","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/file_3","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1\\file_3","file_3","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"5","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_2/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"10","6","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"11","10","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"12","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-04T23:30:30","false","","","","","",""
"13","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_4","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_4","file_4","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"14","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_5","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_5","file_5","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"15","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_6","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_6","file_6","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"16","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"17","16","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-04T23:31:00","false","","","","","",""
"18","17","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/file_7","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1\\file_7","file_7","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"""

SF_LINUX_CSV = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file://archive,/archive,archive,,Done,,Folder,,2023-01-04T23:28:05+01:00,false,,,,,,
2,1,file://archive/sub_dir_1,/archive/sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-04T23:29:44+01:00,false,,,,,,
3,2,file://archive/sub_dir_1/file_1,/archive/sub_dir_1/file_1,file_1,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,2,file://archive/sub_dir_1/file_2,/archive/sub_dir_1/file_2,file_2,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,2,file://archive/sub_dir_1/sub_1_dir_1,/archive/sub_dir_1/sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-04T23:29:54+01:00,false,,,,,,
6,5,file://archive/sub_dir_1/sub_1_dir_1/file_3,/archive/sub_dir_1/sub_1_dir_1/file_3,file_3,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,1,file://archive/sub_dir_2,/archive/sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
8,1,file://archive/sub_dir_3,/archive/sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
9,8,file://archive/sub_dir_3/sub_3_empty_1,/archive/sub_dir_3/sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
10,9,file://archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
11,1,file://archive/sub_dir_4,/archive/sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-04T23:30:30+01:00,false,,,,,,
12,11,file://archive/sub_dir_4/file_4,/archive/sub_dir_4/file_4,file_4,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
13,11,file://archive/sub_dir_4/file_5,/archive/sub_dir_4/file_5,file_5,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
14,11,file://archive/sub_dir_4/file_6,/archive/sub_dir_4/file_6,file_6,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
15,1,file://archive/sub_dir_5,/archive/sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
16,15,file://archive/sub_dir_5/sub_5_dir_1,/archive/sub_dir_5/sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-04T23:31:00+01:00,false,,,,,,
17,16,file://archive/sub_dir_5/sub_5_dir_1/file_7,/archive/sub_dir_5/sub_5_dir_1/file_7,file_7,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
"""

SF_WINDOWS_CSV = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file:/C:/Users/droid_user/sumfolder1/reference/archive,C:\\Users\\droid_user\\sumfolder1\\reference\\archive,archive,,Done,,Folder,,2023-01-05T10:27:00+01:00,false,,,,,,
2,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-04T23:29:44+01:00,false,,,,,,
3,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_1,file_1,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_2,file_2,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-04T23:29:54+01:00,false,,,,,,
6,5,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/file_3,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1\\file_3,file_3,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
8,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
9,8,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
10,9,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
11,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-04T23:30:30+01:00,false,,,,,,
12,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_4,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_4,file_4,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
13,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_5,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_5,file_5,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
14,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_6,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_6,file_6,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
15,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
16,15,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-04T23:31:00+01:00,false,,,,,,
17,16,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/file_7,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1\\file_7,file_7,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
"""


@pytest.mark.parametrize(
    "droid_report,is_windows",
    [
        (DROID_LINUX_CSV, False),
        (SF_WINDOWS_CSV, True),
        (DROID_WINDOWS_CSV, True),
        (SF_LINUX_CSV, False),
    ],
)
def test_existing_root_node(tmp_path, droid_report, is_windows):
    """todo..."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()

    assert folder_sum.folders is None
    assert folder_sum.files is None

    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders is not None
    assert folder_sum.files is not None

    folders_results = []
    for folder in folder_sum.folders:
        folders_results.append(
            f"{folder.path.name} {folder.hash_} {folder.depth} {folder.sort_order}"
        )

    # Sort order should be consistent and so list ordering should be
    # predictable.
    if is_windows:
        expected_folders = [
            "archive 38f27e0641507c124daabe21c08dc4a1 6 0",
            "sub_dir_1 b40a1fc415f761feeeae17d186e9f646 7 2",
            "sub_1_dir_1 ec01eb83265578c6a1ce893964bd64c7 8 5",
            "sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90 7 7",
            "sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e 7 8",
            "sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1 8 9",
            "sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90 9 10",
            "sub_dir_4 e89d20857f3219ad04fa0d9e9c7d266e 7 11",
            "sub_dir_5 a8c13363f1380fd1f29a676d2a73b9af 7 15",
            "sub_5_dir_1 86d324196afb0f709cf5ff59c1b373de 8 16",
        ]
    if not is_windows:
        expected_folders = [
            "archive 38f27e0641507c124daabe21c08dc4a1 2 0",
            "sub_dir_1 b40a1fc415f761feeeae17d186e9f646 3 2",
            "sub_1_dir_1 ec01eb83265578c6a1ce893964bd64c7 4 5",
            "sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90 3 7",
            "sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e 3 8",
            "sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1 4 9",
            "sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90 5 10",
            "sub_dir_4 e89d20857f3219ad04fa0d9e9c7d266e 3 11",
            "sub_dir_5 a8c13363f1380fd1f29a676d2a73b9af 3 15",
            "sub_5_dir_1 86d324196afb0f709cf5ff59c1b373de 4 16",
        ]

    assert folders_results == expected_folders

    files_results = []
    for file in folder_sum.files:
        files_results.append(f"{file.path.name} {file.hash_}")

    # Files are sorted by hash alphanumerically and so the results
    # here, for the reference set should be consistent.
    expected_files = [
        "file_1 14118ff9ad0344decb37960809b2f17a",
        "file_6 2b43227486ec8744cd5d4c955d269743",
        "file_5 637a3fb7da1ab61d10e96336d9758416",
        "file_2 a4501ee1a5c711ea9db78a800a24e830",
        "file_7 c5a1973a70e08bf1eee13b8090f790ad",
        "file_3 dc7f828c5fe622925181d06edada350f",
        "file_4 e3d90a4bf14a9b355f0e69ba08df522d",
    ]

    assert files_results == expected_files
    assert folder_sum.root_folder_hash == "38f27e0641507c124daabe21c08dc4a1"


@pytest.mark.parametrize(
    "droid_report,is_windows",
    [
        (DROID_LINUX_CSV, False),
        (SF_WINDOWS_CSV, True),
        (DROID_WINDOWS_CSV, True),
        (SF_LINUX_CSV, False),
    ],
)
def test_artificial_root_node(tmp_path, droid_report, is_windows):
    """We have an option to create an encapsulating root node
    regardless of whether the dataset is already shaped this way, i.e.
    has an existing root node from which all other branches stem. If we
    trigger this option, we still want it to be correct.
    """
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()

    assert folder_sum.folders is None
    assert folder_sum.files is None

    folder_sum.sum_folders(str(droid_csv), make_root_node=True)

    assert folder_sum.folders is not None
    assert folder_sum.files is not None

    # The hash for our original set still exists, just at a lower
    # level [1]. Now we have another root hash we can refer to [0].
    assert folder_sum.folders[0].hash_ == "0b246bb9e78ea53ab83ea448f02718d1"
    assert folder_sum.folders[1].hash_ == "38f27e0641507c124daabe21c08dc4a1"

    # The new root hash in this instance is just a hash of a single hash
    # which we can test here.
    digest = hashlib.md5()
    digest.update(folder_sum.folders[1].hash_.encode())
    assert digest.hexdigest() == "0b246bb9e78ea53ab83ea448f02718d1"

    assert folder_sum.folders[0].path.name == "merkle_collection_root"
    assert folder_sum.folders[0].sort_order == 0
    assert folder_sum.folders[0].is_root is True

    if is_windows:
        assert folder_sum.folders[0].depth == 5
    else:
        assert folder_sum.folders[0].depth == 1

    assert folder_sum.folders[0].path.name == "merkle_collection_root"
    assert folder_sum.folders[0].sort_order == 0
    assert folder_sum.folders[0].is_root is True

    if is_windows:
        assert folder_sum.folders[0].depth == 5
    else:
        assert folder_sum.folders[0].depth == 1


DROID_LINUX_CSV_NO_ROOT = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"9","2","file:/archive/sub_dir_1/","/archive/sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-04T23:29:44","false","","","","","",""
"18","9","file:/archive/sub_dir_1/file_1","/archive/sub_dir_1/file_1","file_1","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"15","9","file:/archive/sub_dir_1/file_2","/archive/sub_dir_1/file_2","file_2","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"10","9","file:/archive/sub_dir_1/sub_1_dir_1/","/archive/sub_dir_1/sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-04T23:29:54","false","","","","","",""
"12","10","file:/archive/sub_dir_1/sub_1_dir_1/file_3","/archive/sub_dir_1/sub_1_dir_1/file_3","file_3","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"11","2","file:/archive/sub_dir_2/","/archive/sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/archive/sub_dir_3/","/archive/sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"7","6","file:/archive/sub_dir_3/sub_3_empty_1/","/archive/sub_dir_3/sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"8","7","file:/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"5","2","file:/archive/sub_dir_4/","/archive/sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-04T23:30:30","false","","","","","",""
"16","5","file:/archive/sub_dir_4/file_4","/archive/sub_dir_4/file_4","file_4","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"14","5","file:/archive/sub_dir_4/file_5","/archive/sub_dir_4/file_5","file_5","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"17","5","file:/archive/sub_dir_4/file_6","/archive/sub_dir_4/file_6","file_6","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"3","2","file:/archive/sub_dir_5/","/archive/sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"4","3","file:/archive/sub_dir_5/sub_5_dir_1/","/archive/sub_dir_5/sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-04T23:31:00","false","","","","","",""
"13","4","file:/archive/sub_dir_5/sub_5_dir_1/file_7","/archive/sub_dir_5/sub_5_dir_1/file_7","file_7","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"""

DROID_WINDOWS_CSV_NO_ROOT = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"3","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-04T23:29:44","false","","","","","",""
"8","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_1","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_1","file_1","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"9","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_2","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_2","file_2","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"4","3","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-04T23:29:54","false","","","","","",""
"7","4","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/file_3","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1\\file_3","file_3","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"5","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_2/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"10","6","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"11","10","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"12","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-04T23:30:30","false","","","","","",""
"13","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_4","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_4","file_4","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"14","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_5","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_5","file_5","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"15","12","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_6","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_6","file_6","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"16","2","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"17","16","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-04T23:31:00","false","","","","","",""
"18","17","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/file_7","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1\\file_7","file_7","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"""

SF_WINDOWS_CSV_NO_ROOT = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-04T23:29:44+01:00,false,,,,,,
3,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_1,file_1,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/file_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\file_2,file_2,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,2,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-04T23:29:54+01:00,false,,,,,,
6,5,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_1/sub_1_dir_1/file_3,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_1\\sub_1_dir_1\\file_3,file_3,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
8,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
9,8,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
10,9,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_3\\sub_3_empty_1\\sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
11,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-04T23:30:30+01:00,false,,,,,,
12,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_4,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_4,file_4,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
13,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_5,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_5,file_5,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
14,11,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_4/file_6,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_4\\file_6,file_6,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
15,1,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
16,15,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-04T23:31:00+01:00,false,,,,,,
17,16,file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/file_7,C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1\\file_7,file_7,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
"""

SF_LINUX_CSV_NO_ROOT = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,1,file://archive/sub_dir_1,/archive/sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-04T23:29:44+01:00,false,,,,,,
3,2,file://archive/sub_dir_1/file_1,/archive/sub_dir_1/file_1,file_1,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,2,file://archive/sub_dir_1/file_2,/archive/sub_dir_1/file_2,file_2,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,2,file://archive/sub_dir_1/sub_1_dir_1,/archive/sub_dir_1/sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-04T23:29:54+01:00,false,,,,,,
6,5,file://archive/sub_dir_1/sub_1_dir_1/file_3,/archive/sub_dir_1/sub_1_dir_1/file_3,file_3,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,1,file://archive/sub_dir_2,/archive/sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
8,1,file://archive/sub_dir_3,/archive/sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
9,8,file://archive/sub_dir_3/sub_3_empty_1,/archive/sub_dir_3/sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
10,9,file://archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,/archive/sub_dir_3/sub_3_empty_1/sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
11,1,file://archive/sub_dir_4,/archive/sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-04T23:30:30+01:00,false,,,,,,
12,11,file://archive/sub_dir_4/file_4,/archive/sub_dir_4/file_4,file_4,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
13,11,file://archive/sub_dir_4/file_5,/archive/sub_dir_4/file_5,file_5,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
14,11,file://archive/sub_dir_4/file_6,/archive/sub_dir_4/file_6,file_6,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
15,1,file://archive/sub_dir_5,/archive/sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
16,15,file://archive/sub_dir_5/sub_5_dir_1,/archive/sub_dir_5/sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-04T23:31:00+01:00,false,,,,,,
17,16,file://archive/sub_dir_5/sub_5_dir_1/file_7,/archive/sub_dir_5/sub_5_dir_1/file_7,file_7,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
"""


@pytest.mark.parametrize(
    "droid_report,is_windows",
    [
        (SF_WINDOWS_CSV_NO_ROOT, True),
        (DROID_WINDOWS_CSV_NO_ROOT, True),
        (SF_LINUX_CSV_NO_ROOT, False),
        (DROID_LINUX_CSV_NO_ROOT, False),
    ],
)
def test_no_root_node(tmp_path, droid_report, is_windows):
    """Stripped of a root node, the original CSV files should still
    evaluate to the same Root node (Rn) checksum.
    """

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()

    assert folder_sum.folders is None
    assert folder_sum.files is None

    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders is not None
    assert folder_sum.files is not None

    # A cool property of this which we can see here, is that even with
    # the originally named root missing, the hash still evaluates to
    # the same as the original when he hash is there.
    assert folder_sum.folders[0].hash_ == "38f27e0641507c124daabe21c08dc4a1"

    # Some of the introduced properties of the artificial root node are
    # tested below.
    assert folder_sum.folders[0].path.name == "merkle_collection_root"
    assert folder_sum.folders[0].sort_order == 0
    assert folder_sum.folders[0].is_root is True

    if is_windows:
        assert folder_sum.folders[0].depth == 6
    else:
        assert folder_sum.folders[0].depth == 2


DROID_WINDOWS_CSV_NEW_FILE = """
"19","17","file:/C:/Users/droid_user/sumfolder1/reference/archive/sub_dir_5/sub_5_dir_1/file_8","C:\\Users\\droid_user\\sumfolder1\\reference\\archive\\sub_dir_5\\sub_5_dir_1\\file_8","file_8","","Done","10","File","","2023-01-04T23:31:00","false","fdffe4dd2d39c7d9986dbf5c6ec5ad39","0","","","",""
"""


def test_add_file(tmp_path):
    """Adding a file to a dataset gives us the opportunity to test the
    integrity of the original data, i.e. only some data should change.
    We also have an opportunity to probe the dataset by asking about
    a file or folder's existence.
    """

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_WINDOWS_CSV.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == "38f27e0641507c124daabe21c08dc4a1"

    file_7 = "c5a1973a70e08bf1eee13b8090f790ad"
    file_8 = "fdffe4dd2d39c7d9986dbf5c6ec5ad39"  # file that we're adding.

    assert file_7 in [file.hash_ for file in folder_sum.files]
    assert file_8 not in [file.hash_ for file in folder_sum.files]

    folders = folder_sum.folders
    files = folder_sum.files

    match = "637a3fb7da1ab61d10e96336d9758416"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "File"

    match = "14118ff9ad0344decb37960809b2f17a"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "File"

    match = "c5a1973a70e08bf1eee13b8090f790ad"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "File"

    match = "1ccb49edc4e873f1a8affd4bad5e9b90"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "Directory"

    # We have one set of duplicate folders in this hierarchy, test
    # those here.
    multi = res["query"]["results"]
    assert len(multi) == 2
    assert multi[0]["containing_dirs"] != multi[1]["containing_dirs"]

    all_multi = [multi[0]["containing_dirs"], multi[1]["containing_dirs"]]

    res1 = ["38f27e0641507c124daabe21c08dc4a1"]
    res2 = [
        "db9d848b4f83ff3cb3faa4df0a59e3e1",
        "2a60541cede91a36e9dc5bab7a97dd6e",
        "38f27e0641507c124daabe21c08dc4a1",
    ]

    assert res1 in all_multi
    assert res2 in all_multi

    # These folders checksums will be created when the new file is
    # added, but they don't have these checksums to begin. Verify
    # that they are not in the set using the verify function.
    folder_sum_1 = "b97e7f327ac133269f4ada94ff7a1ef8"
    folder_sum_2 = "4ddacbb8a8140315ec15815195e0bb08"

    res = folder_sum.verify_hash(folder_sum_1, folders, files).as_dict()
    assert res["query"]["found"] is False
    assert res["query"]["type"] is None

    res = folder_sum.verify_hash(folder_sum_2, folders, files).as_dict()
    assert res["query"]["found"] is False
    assert res["query"]["type"] is None

    add_file_csv = f"{DROID_WINDOWS_CSV.strip()}\n{DROID_WINDOWS_CSV_NEW_FILE.strip()}"
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(add_file_csv.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == "cec9de95a2236712648c13c61a88604e"

    assert file_7 in [file.hash_ for file in folder_sum.files]
    assert file_8 in [file.hash_ for file in folder_sum.files]
    assert folder_sum_1 in [folder.hash_ for folder in folder_sum.folders]
    assert folder_sum_2 in [folder.hash_ for folder in folder_sum.folders]

    folders = folder_sum.folders
    files = folder_sum.files

    res = folder_sum.verify_hash(folder_sum_1, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "Directory"
    assert len(res["query"]["results"]) == 1
    contained_in = res["query"]["results"][0]["containing_dirs"]
    assert contained_in == ["cec9de95a2236712648c13c61a88604e"]

    res = folder_sum.verify_hash(folder_sum_2, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "Directory"
    assert len(res["query"]["results"]) == 1
    contained_in = res["query"]["results"][0]["containing_dirs"]
    assert contained_in == [
        "b97e7f327ac133269f4ada94ff7a1ef8",
        "cec9de95a2236712648c13c61a88604e",
    ]

    all_new_hashes = [folder.hash_ for folder in folders]
    expected_hashes = [
        "cec9de95a2236712648c13c61a88604e",  # modified by file addition
        "b40a1fc415f761feeeae17d186e9f646",  # same as first run.
        "ec01eb83265578c6a1ce893964bd64c7",  # same as first run.
        "1ccb49edc4e873f1a8affd4bad5e9b90",  # same as first run.
        "2a60541cede91a36e9dc5bab7a97dd6e",  # same as first run.
        "db9d848b4f83ff3cb3faa4df0a59e3e1",  # same as first run.
        "1ccb49edc4e873f1a8affd4bad5e9b90",  # same as first run.
        "e89d20857f3219ad04fa0d9e9c7d266e",  # same as first run.
        "b97e7f327ac133269f4ada94ff7a1ef8",  # modified by file addition
        "4ddacbb8a8140315ec15815195e0bb08",  # modified by file addition
    ]
    assert all_new_hashes == expected_hashes


REFERENCE_SF_LINUX_CSV_NO_EMPTY_FILE = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file://home/siegfried_user/sumfolder1/reference/collection,/home/siegfried_user/sumfolder1/reference/collection,archive,,Done,,Folder,,2023-01-08T18:49:15+01:00,false,,,,,,
2,1,file://home/siegfried_user/sumfolder1/reference/collection/file_0000,/home/siegfried_user/sumfolder1/reference/collection/file_0000,file_0000,Text,Done,10,File,,2023-01-08T18:43:06+01:00,TRUE,8cfda2609b880a553759cd6200823f3b,1,x-fmt/111,text/plain,Plain Text File,
3,1,file://home/siegfried_user/sumfolder1/reference/collection/file_0001,/home/siegfried_user/sumfolder1/reference/collection/file_0001,file_0001,Text,Done,10,File,,2023-01-04T23:29:39+01:00,TRUE,14118ff9ad0344decb37960809b2f17a,1,x-fmt/111,text/plain,Plain Text File,
4,1,file://home/siegfried_user/sumfolder1/reference/collection/file_0002,/home/siegfried_user/sumfolder1/reference/collection/file_0002,file_0002,Text,Done,10,File,,2023-01-04T23:29:44+01:00,TRUE,a4501ee1a5c711ea9db78a800a24e830,1,x-fmt/111,text/plain,Plain Text File,
5,1,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_1,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_1,sub_dir_1,,Done,,Folder,,2023-01-08T18:48:55+01:00,false,,,,,,
6,5,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/file_0003,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/file_0003,file_0003,Text,Done,10,File,,2023-01-04T23:29:54+01:00,TRUE,dc7f828c5fe622925181d06edada350f,1,x-fmt/111,text/plain,Plain Text File,
7,5,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/file_0004,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/file_0004,file_0004,Text,Done,10,File,,2023-01-04T23:30:19+01:00,TRUE,e3d90a4bf14a9b355f0e69ba08df522d,1,x-fmt/111,text/plain,Plain Text File,
8,5,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1,sub_1_dir_1,,Done,,Folder,,2023-01-08T18:49:00+01:00,false,,,,,,
9,8,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005,file_0005,Text,Done,10,File,,2023-01-04T23:30:23+01:00,TRUE,637a3fb7da1ab61d10e96336d9758416,1,x-fmt/111,text/plain,Plain Text File,
10,1,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_2,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_2,sub_dir_2,,Done,,Folder,,2023-01-04T23:27:50+01:00,false,,,,,,
11,1,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_3,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_3,sub_dir_3,,Done,,Folder,,2023-01-04T23:28:39+01:00,false,,,,,,
12,11,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1,sub_3_empty_1,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
13,12,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2,sub_3_empty_2,,Done,,Folder,,2023-01-04T23:28:54+01:00,false,,,,,,
14,1,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_4,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_4,sub_dir_4,,Done,,Folder,,2023-01-08T18:48:43+01:00,false,,,,,,
15,14,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0006,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0006,file_0006,Text,Done,10,File,,2023-01-04T23:30:30+01:00,TRUE,2b43227486ec8744cd5d4c955d269743,1,x-fmt/111,text/plain,Plain Text File,
16,14,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0007,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0007,file_0007,Text,Done,10,File,,2023-01-04T23:31:00+01:00,TRUE,c5a1973a70e08bf1eee13b8090f790ad,1,x-fmt/111,text/plain,Plain Text File,
17,14,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0008,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_4/file_0008,file_0008,Text,Done,10,File,,2023-01-06T00:40:09+01:00,TRUE,fdffe4dd2d39c7d9986dbf5c6ec5ad39,1,x-fmt/111,text/plain,Plain Text File,
18,1,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_5,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_5,sub_dir_5,,Done,,Folder,,2023-01-04T23:30:52+01:00,false,,,,,,
19,18,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1,sub_5_dir_1,,Done,,Folder,,2023-01-08T18:48:24+01:00,false,,,,,,
20,19,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009,file_0009,Text,Done,10,File,,2023-01-08T18:45:46+01:00,TRUE,7c1f9f9a4d0ce9a72ee63f37a1b7f694,1,x-fmt/111,text/plain,Plain Text File,
21,19,file://home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010,/home/siegfried_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010,file_0010,Text,Done,10,File,,2023-01-08T18:45:51+01:00,TRUE,aececec0bc3f515039aec9e60c413cd3,1,x-fmt/111,text/plain,Plain Text File,
"""

REFERENCE_DROID_LINUX_CSV_NO_EMPTY_FILE = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/home/droid_user/sumfolder1/reference/collection/","/home/droid_user/sumfolder1/reference/collection","archive","","Done","","Folder","","2023-01-08T18:49:15","false","","","","","",""
"16","2","file:/home/droid_user/sumfolder1/reference/collection/file_0000","/home/droid_user/sumfolder1/reference/collection/file_0000","file_0000","","Done","10","File","","2023-01-08T18:43:06","false","8cfda2609b880a553759cd6200823f3b","0","","","",""
"15","2","file:/home/droid_user/sumfolder1/reference/collection/file_0001","/home/droid_user/sumfolder1/reference/collection/file_0001","file_0001","","Done","10","File","","2023-01-04T23:29:39","false","14118ff9ad0344decb37960809b2f17a","0","","","",""
"21","2","file:/home/droid_user/sumfolder1/reference/collection/file_0002","/home/droid_user/sumfolder1/reference/collection/file_0002","file_0002","","Done","10","File","","2023-01-04T23:29:44","false","a4501ee1a5c711ea9db78a800a24e830","0","","","",""
"9","2","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_1/","/home/droid_user/sumfolder1/reference/collection/sub_dir_1","sub_dir_1","","Done","","Folder","","2023-01-08T18:48:55","false","","","","","",""
"14","9","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_1/file_0003","/home/droid_user/sumfolder1/reference/collection/sub_dir_1/file_0003","file_0003","","Done","10","File","","2023-01-04T23:29:54","false","dc7f828c5fe622925181d06edada350f","0","","","",""
"13","9","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_1/file_0004","/home/droid_user/sumfolder1/reference/collection/sub_dir_1/file_0004","file_0004","","Done","10","File","","2023-01-04T23:30:19","false","e3d90a4bf14a9b355f0e69ba08df522d","0","","","",""
"10","9","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/","/home/droid_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1","sub_1_dir_1","","Done","","Folder","","2023-01-08T18:49:00","false","","","","","",""
"17","10","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005","/home/droid_user/sumfolder1/reference/collection/sub_dir_1/sub_1_dir_1/file_0005","file_0005","","Done","10","File","","2023-01-04T23:30:23","false","637a3fb7da1ab61d10e96336d9758416","0","","","",""
"11","2","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_2/","/home/droid_user/sumfolder1/reference/collection/sub_dir_2","sub_dir_2","","Empty","","Folder","","2023-01-04T23:27:50","false","","","","","",""
"6","2","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_3/","/home/droid_user/sumfolder1/reference/collection/sub_dir_3","sub_dir_3","","Done","","Folder","","2023-01-04T23:28:39","false","","","","","",""
"7","6","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/","/home/droid_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1","sub_3_empty_1","","Done","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"8","7","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2/","/home/droid_user/sumfolder1/reference/collection/sub_dir_3/sub_3_empty_1/sub_3_empty_2","sub_3_empty_2","","Empty","","Folder","","2023-01-04T23:28:54","false","","","","","",""
"5","2","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_4/","/home/droid_user/sumfolder1/reference/collection/sub_dir_4","sub_dir_4","","Done","","Folder","","2023-01-08T18:48:43","false","","","","","",""
"19","5","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0006","/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0006","file_0006","","Done","10","File","","2023-01-04T23:30:30","false","2b43227486ec8744cd5d4c955d269743","0","","","",""
"18","5","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0007","/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0007","file_0007","","Done","10","File","","2023-01-04T23:31:00","false","c5a1973a70e08bf1eee13b8090f790ad","0","","","",""
"20","5","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0008","/home/droid_user/sumfolder1/reference/collection/sub_dir_4/file_0008","file_0008","","Done","10","File","","2023-01-06T00:40:09","false","fdffe4dd2d39c7d9986dbf5c6ec5ad39","0","","","",""
"3","2","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_5/","/home/droid_user/sumfolder1/reference/collection/sub_dir_5","sub_dir_5","","Done","","Folder","","2023-01-04T23:30:52","false","","","","","",""
"4","3","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/","/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1","sub_5_dir_1","","Done","","Folder","","2023-01-08T18:48:24","false","","","","","",""
"22","4","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009","/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0009","file_0009","","Done","10","File","","2023-01-08T18:45:46","false","7c1f9f9a4d0ce9a72ee63f37a1b7f694","0","","","",""
"12","4","file:/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010","/home/droid_user/sumfolder1/reference/collection/sub_dir_5/sub_5_dir_1/file_0010","file_0010","","Done","10","File","","2023-01-08T18:45:51","false","aececec0bc3f515039aec9e60c413cd3","0","","","",""

"""


@pytest.mark.parametrize(
    "droid_report",
    [
        (REFERENCE_DROID_LINUX_CSV_NO_EMPTY_FILE),
        (REFERENCE_SF_LINUX_CSV_NO_EMPTY_FILE),
    ],
)
def test_reference_no_empties(tmp_path, droid_report):
    """Test the reference set as described by the following layout:

    📁 archive d31d760c55a6971e8fa4a9f7c717d324 (0) (8)
    📄 file_0001 14118ff9ad0344decb37960809b2f17a
    📄 file_0000 8cfda2609b880a553759cd6200823f3b
    📄 file_0002 a4501ee1a5c711ea9db78a800a24e830
    📁 sub_dir_1 d7150a51f676408dc9120d2d1ded1cd6 (5) (9)
       📄 file_0003 dc7f828c5fe622925181d06edada350f
       📄 file_0004 e3d90a4bf14a9b355f0e69ba08df522d
       📁 sub_1_dir_1 1c7ba27edf1356d097a3f568032430c2 (8) (10)
          📄 file_0005 637a3fb7da1ab61d10e96336d9758416
    📁 sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90 (10) (9)
    📁 sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e (11) (9)
       📁 sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1 (12) (10)
          📁 sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90 (13) (11)
    📁 sub_dir_4 272d45767d534335163f220c1d40e559 (14) (9)
       📄 file_0006 2b43227486ec8744cd5d4c955d269743
       📄 file_0007 c5a1973a70e08bf1eee13b8090f790ad
       📄 file_0008 fdffe4dd2d39c7d9986dbf5c6ec5ad39
    📁 sub_dir_5 d818d29b75f89a9b5d8d1c5a4c70dbbb (18) (9)
       📁 sub_5_dir_1 82f9e9a4305714fffdd7932783980cbc (19) (10)
          📄 file_0009 7c1f9f9a4d0ce9a72ee63f37a1b7f694
          📄 file_0010 aececec0bc3f515039aec9e60c413cd3

    """
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == "d31d760c55a6971e8fa4a9f7c717d324"


def calculate(digests):
    """Calculate a digest for a given list."""
    digest = hashlib.md5()
    for item in digests:
        digest.update(item)
    return digest.hexdigest()


def test_reference_no_empties_standalone():
    """Standalone test that sums the reference dataset independently
     of the script.

    📁 archive d31d760c55a6971e8fa4a9f7c717d324 (0) (8)
    📄 file_0001 14118ff9ad0344decb37960809b2f17a
    📄 file_0000 8cfda2609b880a553759cd6200823f3b
    📄 file_0002 a4501ee1a5c711ea9db78a800a24e830
    📁 sub_dir_1 d7150a51f676408dc9120d2d1ded1cd6 (5) (9)
       📄 file_0003 dc7f828c5fe622925181d06edada350f
       📄 file_0004 e3d90a4bf14a9b355f0e69ba08df522d
       📁 sub_1_dir_1 1c7ba27edf1356d097a3f568032430c2 (8) (10)
          📄 file_0005 637a3fb7da1ab61d10e96336d9758416
    📁 sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90 (10) (9)
    📁 sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e (11) (9)
       📁 sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1 (12) (10)
          📁 sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90 (13) (11)
    📁 sub_dir_4 272d45767d534335163f220c1d40e559 (14) (9)
       📄 file_0006 2b43227486ec8744cd5d4c955d269743
       📄 file_0007 c5a1973a70e08bf1eee13b8090f790ad
       📄 file_0008 fdffe4dd2d39c7d9986dbf5c6ec5ad39
    📁 sub_dir_5 d818d29b75f89a9b5d8d1c5a4c70dbbb (18) (9)
       📁 sub_5_dir_1 82f9e9a4305714fffdd7932783980cbc (19) (10)
          📄 file_0009 7c1f9f9a4d0ce9a72ee63f37a1b7f694
          📄 file_0010 aececec0bc3f515039aec9e60c413cd3

    """

    sub_5_dir_1 = [
        b"7c1f9f9a4d0ce9a72ee63f37a1b7f694",
        b"aececec0bc3f515039aec9e60c413cd3",
    ]
    expected_res_sub_5_dir_1 = "82f9e9a4305714fffdd7932783980cbc"
    assert calculate(sub_5_dir_1) == expected_res_sub_5_dir_1

    sub_dir_5 = [b"82f9e9a4305714fffdd7932783980cbc"]
    expected_res_sub_dir_5 = "d818d29b75f89a9b5d8d1c5a4c70dbbb"
    assert calculate(sub_dir_5) == expected_res_sub_dir_5

    sub_dir_4 = [
        b"2b43227486ec8744cd5d4c955d269743",
        b"c5a1973a70e08bf1eee13b8090f790ad",
        b"fdffe4dd2d39c7d9986dbf5c6ec5ad39",
    ]
    expected_sub_dir_4 = "272d45767d534335163f220c1d40e559"
    assert calculate(sub_dir_4) == expected_sub_dir_4

    sub_3_empty_2 = [b"1ccb49edc4e873f1a8affd4bad5e9b90"]
    expected_sub_3_empty_1 = "db9d848b4f83ff3cb3faa4df0a59e3e1"
    assert calculate(sub_3_empty_2) == expected_sub_3_empty_1

    sub_dir_3 = [b"db9d848b4f83ff3cb3faa4df0a59e3e1"]
    expected_sub_dir_3 = "2a60541cede91a36e9dc5bab7a97dd6e"
    assert calculate(sub_dir_3) == expected_sub_dir_3

    # Sub dir 2 isn't calculated...
    sub_dir_2 = "1ccb49edc4e873f1a8affd4bad5e9b90"
    assert sub_dir_2 == sub_dir_2  # pylint: disable=R0124

    sub_1_dir_1 = [b"637a3fb7da1ab61d10e96336d9758416"]
    expected_sub_1_dir_1 = "1c7ba27edf1356d097a3f568032430c2"
    assert calculate(sub_1_dir_1) == expected_sub_1_dir_1

    sub_dir_1 = [
        b"1c7ba27edf1356d097a3f568032430c2",
        b"dc7f828c5fe622925181d06edada350f",
        b"e3d90a4bf14a9b355f0e69ba08df522d",
    ]
    expected_sub_dir_1 = "d7150a51f676408dc9120d2d1ded1cd6"
    assert calculate(sub_dir_1) == expected_sub_dir_1

    collection = [
        b"d818d29b75f89a9b5d8d1c5a4c70dbbb",
        b"272d45767d534335163f220c1d40e559",
        b"2a60541cede91a36e9dc5bab7a97dd6e",
        b"1ccb49edc4e873f1a8affd4bad5e9b90",
        b"d7150a51f676408dc9120d2d1ded1cd6",
        b"14118ff9ad0344decb37960809b2f17a",
        b"8cfda2609b880a553759cd6200823f3b",
        b"a4501ee1a5c711ea9db78a800a24e830",
    ]

    res_collection = "d31d760c55a6971e8fa4a9f7c717d324"
    assert calculate(collection) == res_collection


DROID_ONE_FILE = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/C:/temp/sumfolder1/sumfolder1.png","C:\\temp\\sumfolder1\\sumfolder1.png","sumfolder1.png","Signature","Done","21666","File","png","2023-01-13T09:34:52","false","07885f23917aa18933289ec0cb2543eb","1","fmt/13","image/png","Portable Network Graphics","1.2"
"""

DROID_TWO_FILES = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"3","","file:/C:/temp/sumfolder1/sumfolder2.png","C:\\temp\\gifs\\sumfolder1\\sumfolder2.png","sumfolder2.png","Signature","Done","44888","File","png","2023-01-13T09:31:00","false","6ebcc9b13db13f5a4c21993dd373c969","1","fmt/12","image/png","Portable Network Graphics","1.1"
"2","","file:/C:/temp/sumfolder1/sumfolder1.png","C:\\temp\\gifs\\sumfolder1\\sumfolder1.png","sumfolder1.png","Signature","Done","21666","File","png","2023-01-13T09:34:52","false","07885f23917aa18933289ec0cb2543eb","1","fmt/13","image/png","Portable Network Graphics","1.2"
"""

SF_ONE_FILE = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,1,file:/C:/temp/sumfolder1/sumfolder1.png,C:\temp\\sumfolder1\\sumfolder1.png,sumfolder1.png,Signature,Done,21666,File,png,2023-01-13T09:34:52+01:00,FALSE,07885f23917aa18933289ec0cb2543eb,1,fmt/13,image/png,Portable Network Graphics,1.2
"""

SF_TWO_FILES = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
2,1,file:/C:/temp/sumfolder1/sumfolder2.png,C:\temp\\sumfolder1\\sumfolder2.png,sumfolder2.png,Signature,Done,44888,File,png,2023-01-13T09:31:00+01:00,FALSE,6ebcc9b13db13f5a4c21993dd373c969,1,fmt/12,image/png,Portable Network Graphics,1.1
3,1,file:/C:/temp/sumfolder1/sumfolder1.png,C:\temp\\sumfolder1\\sumfolder1.png,sumfolder1.png,Signature,Done,21666,File,png,2023-01-13T09:34:52+01:00,FALSE,07885f23917aa18933289ec0cb2543eb,1,fmt/13,image/png,Portable Network Graphics,1.2
"""


@pytest.mark.parametrize(
    "droid_report,result,one_file",
    [
        (DROID_ONE_FILE, "e4f214bab1f76711c0e3474dbe2d4090", True),
        (DROID_TWO_FILES, "afb6bb1fff93217eb4c4bbfb3f63b8c6", False),
        (SF_ONE_FILE, "e4f214bab1f76711c0e3474dbe2d4090", True),
        (SF_TWO_FILES, "afb6bb1fff93217eb4c4bbfb3f63b8c6", False),
    ],
)
def test_only_files(tmp_path, droid_report, result, one_file):
    """Test the behaviour of the tool when there is no root folder and
    one files in the report.
    """

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == result
    assert folder_sum.folders[0].path.name == "merkle_collection_root"

    # Because we want to be absolutely rigorous, but also, ensure that
    # folks can learn from this script, test the expected results
    # individually for a single file (the hash of itself), and two
    # files, i.e. their combined hash, created in alphabetical order.
    one_digest = hashlib.md5()
    two_digests = hashlib.md5()
    digests = ["07885f23917aa18933289ec0cb2543eb", "6ebcc9b13db13f5a4c21993dd373c969"]
    if one_file:
        one_digest.update(digests[0].encode())
        assert one_digest.hexdigest() == result
    else:
        for digest in digests:
            two_digests.update(digest.encode())
        assert two_digests.hexdigest() == result


SF_EMPTY_DIR = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file:/C:/sumfolder1/empty,C:\\sumfolder1\\empty,empty,,Done,,Folder,,2023-01-13T12:16:37+01:00,false,,,,,,
"""

DROID_EMPTY_DIR = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/C:/sumfolder1/empty/","C:\\sumfolder1\\empty","empty","","Empty","","Folder","","2023-01-13T12:16:37","false","","","","","",""
"""


@pytest.mark.parametrize(
    "droid_report",
    [
        (SF_EMPTY_DIR),
        (DROID_EMPTY_DIR),
    ],
)
def test_one_empty_folder(tmp_path, droid_report):
    """Ensure that the result for one empty folder is as expected. I.e.
    our custom empty folder hash.
    """

    folder_str = Folder().EMPTY_DIR
    assert folder_str == b"2600_EMPTY_DIRECTORY"
    digest = hashlib.md5()
    digest.update(folder_str)

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == digest.hexdigest()


SF_DUPES = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file:/C:/sumfolder1,C:\\sumfolder1,sumfolder1,,Done,,Folder,,2023-01-13T12:40:44+01:00,false,,,,,,
2,1,file:/C:/sumfolder1/level_0_empty,C:\\sumfolder1\\level_0_empty,level_0_empty,,Done,,Folder,,2023-01-13T12:40:26+01:00,false,,,,,,
3,1,file:/C:/sumfolder1/level_1,C:\\sumfolder1\\level_1,level_1,,Done,,Folder,,2023-01-13T12:40:53+01:00,false,,,,,,
4,3,file:/C:/sumfolder1/level_1/level_1_empty,C:\\sumfolder1\\level_1\\level_1_empty,level_1_empty,,Done,,Folder,,2023-01-13T12:40:49+01:00,false,,,,,,
5,3,file:/C:/sumfolder1/level_1/level_2,C:\\sumfolder1\\level_1\\level_2,level_2,,Done,,Folder,,2023-01-13T12:41:01+01:00,false,,,,,,
6,5,file:/C:/sumfolder1/level_1/level_2/level_2_empty,C:\\sumfolder1\\level_1\\level_2\\level_2_empty,level_2_empty,,Done,,Folder,,2023-01-13T12:40:57+01:00,false,,,,,,
7,5,file:/C:/sumfolder1/level_1/level_2/sumfolder1.png,C:\\sumfolder1\\level_1\\level_2\\sumfolder1.png,sumfolder1.png,Signature,Done,21666,File,png,2023-01-13T09:34:52+01:00,FALSE,07885f23917aa18933289ec0cb2543eb,1,fmt/13,image/png,Portable Network Graphics,1.2
8,3,file:/C:/sumfolder1/level_1/sumfolder1.png,C:\\sumfolder1\\level_1\\sumfolder1.png,sumfolder1.png,Signature,Done,21666,File,png,2023-01-13T09:34:52+01:00,FALSE,07885f23917aa18933289ec0cb2543eb,1,fmt/13,image/png,Portable Network Graphics,1.2
9,1,file:/C:/sumfolder1/sumfolder1.png,C:\\sumfolder1\\sumfolder1.png,sumfolder1.png,Signature,Done,21666,File,png,2023-01-13T09:34:52+01:00,FALSE,07885f23917aa18933289ec0cb2543eb,1,fmt/13,image/png,Portable Network Graphics,1.2
"""

DROID_DUPES = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/C:/sumfolder1/","C:\\sumfolder1","sumfolder1","","Done","","Folder","","2023-01-13T12:40:44","false","","","","","",""
"3","2","file:/C:/sumfolder1/level_0_empty/","C:\\sumfolder1\\level_0_empty","level_0_empty","","Empty","","Folder","","2023-01-13T12:40:26","false","","","","","",""
"4","2","file:/C:/sumfolder1/level_1/","C:\\sumfolder1\\level_1","level_1","","Done","","Folder","","2023-01-13T12:40:53","false","","","","","",""
"5","4","file:/C:/sumfolder1/level_1/level_1_empty/","C:\\sumfolder1\\level_1\\level_1_empty","level_1_empty","","Empty","","Folder","","2023-01-13T12:40:49","false","","","","","",""
"6","4","file:/C:/sumfolder1/level_1/level_2/","C:\\sumfolder1\\level_1\\level_2","level_2","","Done","","Folder","","2023-01-13T12:41:01","false","","","","","",""
"7","6","file:/C:/sumfolder1/level_1/level_2/level_2_empty/","C:\\sumfolder1\\level_1\\level_2\\level_2_empty","level_2_empty","","Empty","","Folder","","2023-01-13T12:40:57","false","","","","","",""
"8","6","file:/C:/sumfolder1/level_1/level_2/sumfolder1.png","C:\\sumfolder1\\level_1\\level_2\\sumfolder1.png","sumfolder1.png","Signature","Done","21666","File","png","2023-01-13T09:34:52","false","07885f23917aa18933289ec0cb2543eb","1","fmt/13","image/png","Portable Network Graphics","1.2"
"9","4","file:/C:/sumfolder1/level_1/sumfolder1.png","C:\\sumfolder1\\level_1\\sumfolder1.png","sumfolder1.png","Signature","Done","21666","File","png","2023-01-13T09:34:52","false","07885f23917aa18933289ec0cb2543eb","1","fmt/13","image/png","Portable Network Graphics","1.2"
"10","2","file:/C:/sumfolder1/sumfolder1.png","C:\\sumfolder1\\sumfolder1.png","sumfolder1.png","Signature","Done","21666","File","png","2023-01-13T09:34:52","false","07885f23917aa18933289ec0cb2543eb","1","fmt/13","image/png","Portable Network Graphics","1.2"
"""


@pytest.mark.parametrize(
    "droid_report",
    [
        (SF_DUPES),
        (DROID_DUPES),
    ],
)
def test_duplicate_pathways(tmp_path, droid_report):
    """Ensure that duplicates are reported and their pathways look
    good.
    """
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    assert folder_sum.folders[0].hash_ == "efa3947f05c0b346f9b65f494681c4e0"

    folders = folder_sum.folders
    files = folder_sum.files

    match = "1ccb49edc4e873f1a8affd4bad5e9b90"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "Directory"

    assert len(res["query"]["results"]) == 3
    contained_in = res["query"]["results"]

    expected_1 = ["efa3947f05c0b346f9b65f494681c4e0"]
    expected_2 = [
        "f9048be615895cb48bcf41eb93170c86",
        "efa3947f05c0b346f9b65f494681c4e0",
    ]
    expected_3 = [
        "5bc1453c8e40a69d32af6c1265095a2d",
        "f9048be615895cb48bcf41eb93170c86",
        "efa3947f05c0b346f9b65f494681c4e0",
    ]

    expected = [
        expected_1,
        expected_2,
        expected_3,
    ]

    for container in contained_in:
        result = container["containing_dirs"]
        assert result in expected

    match = "07885f23917aa18933289ec0cb2543eb"
    res = folder_sum.verify_hash(match, folders, files).as_dict()
    assert res["query"]["found"] is True
    assert res["query"]["type"] == "File"

    assert len(res["query"]["results"]) == 3
    contained_in = res["query"]["results"]

    expected_1 = [
        "5bc1453c8e40a69d32af6c1265095a2d",
        "f9048be615895cb48bcf41eb93170c86",
        "efa3947f05c0b346f9b65f494681c4e0",
    ]
    expected_2 = [
        "f9048be615895cb48bcf41eb93170c86",
        "efa3947f05c0b346f9b65f494681c4e0",
    ]
    expected_3 = ["efa3947f05c0b346f9b65f494681c4e0"]

    expected = [
        expected_1,
        expected_2,
        expected_3,
    ]

    for container in contained_in:
        result = container["containing_dirs"]
        assert result in expected
