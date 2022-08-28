import dailybkup.testutils as testutils
from dailybkup.testutils import p


class TestFUnctionalB2Context():

    def test_upload_and_erase_file(self):
        with testutils.b2_test_setup() as context:
            context.upload(p("file1"), "foo")
            assert context.count_files() == 1
            context.delete("foo")
            assert context.count_files() == 0
