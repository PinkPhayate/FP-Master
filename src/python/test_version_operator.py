from Model import stub
import version_operator as vo
def test_adjust_bug_list(model):
    vo.adjust_bug_list(model)

model = stub.get_derby_bug_adjust_model()
test_adjust_bug_list(model)
