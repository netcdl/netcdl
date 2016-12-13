
from Test import Test

class TestTest:

    def test_ctor(self):
        t = Test('statement')
        assert t.statement == 'statement'
        assert t.success == False


    def test_create_result(self):
        t = Test('statement')
        result = t.create_result()
        assert result.passed == t.success
        assert result.display_str == t.display_str
        assert result.result_detail == t.result_detail


    def test_to_str(self):
        t = Test('statement')
        assert str(t) == "display success:False detail:default detail"







