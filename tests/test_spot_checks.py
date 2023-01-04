"""Additional tests that we can accumulate based on user-testing."""

import hashlib

from src.sumfolder1.sumfolders import SumFolders

ALPHABET_TEST_CSV = """
ID,PARENT_ID,URI,FILE_PATH,NAME,METHOD,STATUS,SIZE,TYPE,EXT,LAST_MODIFIED,EXTENSION_MISMATCH,MD5_HASH,FORMAT_COUNT,PUID,MIME_TYPE,FORMAT_NAME,FORMAT_VERSION
1,,file://tmp/alphabet_test,/tmp/alphabet_test,alphabet_test,,Done,,Folder,,2023-01-15T14:39:19+01:00,false,,,,,,
2,1,file://tmp/alphabet_test/dir_a,/tmp/alphabet_test/dir_a,dir_a,,Done,,Folder,,2023-01-15T14:39:30+01:00,false,,,,,,
3,2,file://tmp/alphabet_test/dir_a/file_a,/tmp/alphabet_test/dir_a/file_a,file_a,Text,Done,2,File,,2023-01-15T14:39:30+01:00,TRUE,60b725f10c9c85c70d97880dfe8191b3,1,x-fmt/111,text/plain,Plain Text File,
4,1,file://tmp/alphabet_test/dir_e,/tmp/alphabet_test/dir_e,dir_e,,Done,,Folder,,2023-01-15T14:39:41+01:00,false,,,,,,
5,4,file://tmp/alphabet_test/dir_e/file_e,/tmp/alphabet_test/dir_e/file_e,file_e,Text,Done,2,File,,2023-01-15T14:39:41+01:00,TRUE,9ffbf43126e33be52cd2bf7e01d627f9,1,x-fmt/111,text/plain,Plain Text File,
6,1,file://tmp/alphabet_test/dir_s,/tmp/alphabet_test/dir_s,dir_s,,Done,,Folder,,2023-01-15T14:40:00+01:00,false,,,,,,
7,6,file://tmp/alphabet_test/dir_s/file_s,/tmp/alphabet_test/dir_s/file_s,file_s,Text,Done,2,File,,2023-01-15T14:40:00+01:00,TRUE,f4d5d0c0671be202bc241807c243e80b,1,x-fmt/111,text/plain,Plain Text File,
8,1,file://tmp/alphabet_test/dir_t,/tmp/alphabet_test/dir_t,dir_t,,Done,,Folder,,2023-01-15T14:40:10+01:00,false,,,,,,
9,8,file://tmp/alphabet_test/dir_t/file_t,/tmp/alphabet_test/dir_t/file_t,file_t,Text,Done,2,File,,2023-01-15T14:40:10+01:00,TRUE,b7269fa2508548e4032c455818f1e321,1,x-fmt/111,text/plain,Plain Text File,
10,1,file://tmp/alphabet_test/dir_x,/tmp/alphabet_test/dir_x,dir_x,,Done,,Folder,,2023-01-15T14:40:19+01:00,false,,,,,,
11,10,file://tmp/alphabet_test/dir_x/file_x,/tmp/alphabet_test/dir_x/file_x,file_x,Text,Done,2,File,,2023-01-15T14:40:19+01:00,TRUE,401b30e3b8b5d629635a5c613cdb7919,1,x-fmt/111,text/plain,Plain Text File,
12,1,file://tmp/alphabet_test/dir_y,/tmp/alphabet_test/dir_y,dir_y,,Done,,Folder,,2023-01-15T14:40:31+01:00,false,,,,,,
13,12,file://tmp/alphabet_test/dir_y/dir_y,/tmp/alphabet_test/dir_y/dir_y,dir_y,Text,Done,2,File,,2023-01-15T14:40:31+01:00,TRUE,009520053b00386d1173f3988c55d192,1,x-fmt/111,text/plain,Plain Text File,
14,1,file://tmp/alphabet_test/dir_z,/tmp/alphabet_test/dir_z,dir_z,,Done,,Folder,,2023-01-15T14:40:45+01:00,false,,,,,,
15,14,file://tmp/alphabet_test/dir_z/file_z,/tmp/alphabet_test/dir_z/file_z,file_z,Text,Done,2,File,,2023-01-15T14:40:45+01:00,TRUE,a8a78d0ff555c931f045b6f448129846,1,x-fmt/111,text/plain,Plain Text File,
"""


def test_alphanumeric_ordering(tmp_path):
    """Ensure that directory names are in alphabetical order."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(ALPHABET_TEST_CSV.strip(), encoding="UTF-8")

    folder_sum = SumFolders()
    folder_sum.sum_folders(str(droid_csv))

    root_hash = "44d24882358cb5c2e3bb104adbe02269"
    assert folder_sum.folders[0].hash_ == root_hash

    hashes = [
        folder.hash_ for folder in folder_sum.folders if folder.hash_ != root_hash
    ]
    expected = [
        "13f506e982b57c54057e88860be250f6",  # a
        "48de911b17076fc52e6e7951f0e0cf31",  # e
        "8b6e01a4c1dd5ad43ecd33c554a95736",  # s
        "7aeb02c7d5c8a55d6d78383f67bc6d62",  # t
        "078b0dfa7c61da6f98894fa286d506de",  # x
        "7eeb19c08b08933d7e36932a487e173f",  # y
        "3436bba5ec29ec325d35aacc11a9d7b7",  # z
    ]
    assert hashes == expected

    digest_1 = hashlib.md5()
    digest_1.update(b"009520053b00386d1173f3988c55d192")
    res_1 = digest_1.hexdigest()
    assert res_1 in expected

    digest_2 = hashlib.md5()
    digest_2.update(b"a8a78d0ff555c931f045b6f448129846")
    res_2 = digest_1.hexdigest()
    assert res_2 in expected

    # Folders are given a sort number alphabetically in order, and then
    # reversed to create the root hash. So the process order looks as
    # follows.
    process_order = [
        "3436bba5ec29ec325d35aacc11a9d7b7",  # z
        "7eeb19c08b08933d7e36932a487e173f",  # y
        "078b0dfa7c61da6f98894fa286d506de",  # x
        "7aeb02c7d5c8a55d6d78383f67bc6d62",  # t
        "8b6e01a4c1dd5ad43ecd33c554a95736",  # s
        "48de911b17076fc52e6e7951f0e0cf31",  # e
        "13f506e982b57c54057e88860be250f6",  # a
    ]
    digest_3 = hashlib.md5()
    for hash_ in process_order:
        digest_3.update(hash_.encode())
    # Ensure that the folders in process order equal the root hash.
    assert digest_3.hexdigest() == root_hash
