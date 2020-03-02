import base64
import os
import sys

sys.path.append("../")


def prj_validation():
    verified_output = open('verified.prj', 'rb')
    verified_prj_read = verified_output.read()
    encoded_verified_output = base64.encodebytes(verified_prj_read)

    command = "python3 ../../exe/prjbuild.py -i shapes.png -o test_output.prj"
    os.system(command)

    built_prj = open("test_output.prj", 'rwb')
    built_prj_read = built_prj.read()
    encoded_post_image_prj = base64.encodebytes(built_prj_read)

    empty_prj = open('empty.prj', 'rb')
    empty_prj_read = empty_prj.read()
    built_prj.write(empty_prj_read)

    assert encoded_verified_output == encoded_post_image_prj


prj_validation()
