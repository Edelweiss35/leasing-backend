from backend.clause_analyze import get_alphacontent

def test_get_alphacontent_for_none():
    assert get_alphacontent("it", "6. this is testing  A. this is testing (i) check it") == None

def test_get_alpha_content_for_a_clause():
    assert get_alphacontent("this is", "6. this is testing  A. this is 1.1 Testing").groups()[0] == "this is testing  A. this is "
