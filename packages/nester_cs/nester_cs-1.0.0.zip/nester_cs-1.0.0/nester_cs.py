"""����"nester.py"ģ��,�ṩ��һ����Ϊprint_lol()�ĺ�������������������Ǵ�ӡ�б�
�����п��ܰ���(Ҳ���ܲ�����)Ƕ���б�"""
def print_lol(the_list):
    """�������ȡһ��λ�ò�������Ϊ"the_list",��������κ�Python�б�(Ҳ�����ǰ���
Ƕ���б���б�)�����ƶ����б��е�ÿ���������(�ݹ��)�������Ļ�ϣ����������ռһ�С�"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print print_lol(each_item)
        else:
            print(each_item)
