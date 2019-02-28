import unittest,json
from test_suite.send_method import SendMethod
# 创建测试类
class StudentManage(unittest.TestCase):
    def setUp(self):
        self.run = SendMethod()
        self.url = "http://127.0.0.1:8000/api/departments/"
    def test_case_01(self):
        """查询学院"""
        data = {
            "master_name": "老皮"
        }
        res = self.run.run_main('get',url=self.url,data=data)
        # print(res)
        # print(type(res))
        master_name = res['results'][0]['master_name']
        # print(master_name)
        print(self.assertEqual(master_name,"老皮","查询失败"))

    def test_case_02(self):
        """新增学院"""
        data = {
            "data": [
                        {
                            "dep_id": "T01",
                            "dep_name": "接口自动化测试学院",
                            "master_name": "郭老师",
                            "slogan": "上课不睡觉"
                        }
                    ]
                }
        res = self.run.run_main('post',url=self.url,jsons=data)
        #print(res)
        dep_id = res["create_success"]["results"][0]["dep_id"]
        #print(dep_id)
        self.assertEqual(dep_id,"T01","新建失败")
    def test_case_03(self):
        """修改学院"""
        data = {
            "data": [
                {
                    "dep_id": "T01",
                    "dep_name": "测试",
                    "master_name": "郭老师",
                    "slogan": "上课不睡觉"
                }
            ]
        }
        url = self.url + 'T01/'
        res = self.run.run_main('put', url=url, jsons=data)
        #print(res)
        dep_name = res["dep_name"]
        # print(dep_id)
        self.assertEqual(dep_name, "测试", "新建失败")
    def test_case_04(self):
        """删除学院"""
        data = {
            "$dep_id_list":"T01"
        }
        res = self.run.run_main('delete',url=self.url,data=data)
        self.assertEqual(res,204,"删除失败")


if __name__ == '__main__':
    unittest.main()

