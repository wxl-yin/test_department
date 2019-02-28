import requests,json
"""
接口测试封装思路:
1.封装每种请求方式
2.封装取值
3.每一个流程作为一个对象
"""
class SendMethod:
    def _send_get(self,url,data=None):
        """get请求"""
        response = requests.get(url, params=data).json()
        #res = json.dumps(response, indent=2, ensure_ascii=False)
        return response
    def _send_post(self,url,data=None,jsons=None):
        """post请求"""
        response = requests.post(url,data=data,json=jsons).json()
        #res = json.dumps(response,indent=2,ensure_ascii=False)
        #status_code = requests.post(url,data=data,json=jsons).status_code
        return response
    def _send_put(self,url,data=None,jsons=None):
        """put请求"""
        response = requests.put(url, data=data, json=jsons).json()
        #res = json.dumps(response, indent=2, ensure_ascii=False)
        return response
    def _send_delete(self,url,data=None):
        """delete请求"""
        response = requests.delete(url, params=data)
        return response.status_code

    def run_main(self,method,url,data=None,jsons=None):
        res = None
        if method == 'get':
            res = self._send_get(url,data=data)
        elif method == 'post':
            res = self._send_post(url,data=data,jsons=jsons)
        elif method == 'put':
            res = self._send_put(url,data=data,jsons=jsons)
        else:
            res = self._send_delete(url,data=data)
        return res

if __name__ == '__main__':
    run = SendMethod()
    """get请求"""
    # url = "http://127.0.0.1:8000/api/departments/"
    # data = {
    #     "master_name": "郭老师"
    # }
    # result = run_main('get',url=url,data=data)
    # print(result)
    """post请求"""
    url = "http://127.0.0.1:8000/api/departments/"
    # 3.定义传入参数
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
    result = run.run_main('post', url=url, jsons=data)
    print(result)