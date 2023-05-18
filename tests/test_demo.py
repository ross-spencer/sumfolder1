"""Ensure the demo output is output consistently. This is used to help
make the README documentation consistent.

📁 collection 93778c524035d5d3e429a2fe43b7700a
   📄 file_0001 14118ff9ad0344decb37960809b2f17a
   📄 file_0000 8cfda2609b880a553759cd6200823f3b
   📄 file_0002 a4501ee1a5c711ea9db78a800a24e830
   📁 sub_dir_1 82301616d7e24f474dbe21de93af0a34
      📄 file_empty d41d8cd98f00b204e9800998ecf8427e
      📄 file_0003 dc7f828c5fe622925181d06edada350f
      📄 file_0004 e3d90a4bf14a9b355f0e69ba08df522d
      📁 sub_1_dir_1 1c7ba27edf1356d097a3f568032430c2
         📄 file_0005 637a3fb7da1ab61d10e96336d9758416
   📁 sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90
   📁 sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e
      📁 sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1
         📁 sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90
   📁 sub_dir_4 272d45767d534335163f220c1d40e559
      📄 file_0006 2b43227486ec8744cd5d4c955d269743
      📄 file_0007 c5a1973a70e08bf1eee13b8090f790ad
      📄 file_0008 fdffe4dd2d39c7d9986dbf5c6ec5ad39
   📁 sub_dir_5 d818d29b75f89a9b5d8d1c5a4c70dbbb
      📁 sub_5_dir_1 82f9e9a4305714fffdd7932783980cbc
         📄 file_0009 7c1f9f9a4d0ce9a72ee63f37a1b7f694
         📄 file_0010 aececec0bc3f515039aec9e60c413cd3
   📁 sub_dir_6 74be16979710d4c4e7c6647856088456
      📄 file_empty d41d8cd98f00b204e9800998ecf8427e

"""

import hashlib
from typing import Final

import pytest

from src.sumfolder1.sumfolders import SumFolders

REFERENCE_SET: Final[
    str
] = """
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


@pytest.mark.parametrize(
    "droid_report",
    [
        (REFERENCE_SET),
    ],
)
def test_demo_set(tmp_path, droid_report):
    """Test the demo set."""
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(droid_report.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    res: Final[str] = "93778c524035d5d3e429a2fe43b7700a"

    assert folder_sum.folders[0].hash_ == res

    demo_sums = [
        # Folders.
        "1ccb49edc4e873f1a8affd4bad5e9b90",
        "272d45767d534335163f220c1d40e559",
        "2a60541cede91a36e9dc5bab7a97dd6e",
        "74be16979710d4c4e7c6647856088456",
        "82301616d7e24f474dbe21de93af0a34",
        "d818d29b75f89a9b5d8d1c5a4c70dbbb",
        # Files.
        "14118ff9ad0344decb37960809b2f17a",
        "8cfda2609b880a553759cd6200823f3b",
        "a4501ee1a5c711ea9db78a800a24e830",
    ]

    demo_digest = hashlib.md5()
    for hash_ in demo_sums:
        demo_digest.update(hash_.encode())
    # Ensure that the folders in process order equal the root hash.
    assert demo_digest.hexdigest() == res
