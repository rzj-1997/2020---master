import time
import csv

MAX_LENGTH = 14
MIN_LENGTH = 4  # 当前版本最小值只能为4，切勿改动
test_data_name = "Example1.csv"
result_file_name = "result.txt"
tribe = []  # 邻接表,前半部分表示部落A
Asize = 0  # 部落A的大小
Bsize = 0  # 部落B的大小
circleCounts = [0] * 6  # [长度4，长度6，长度8，长度10，长度12，长度14]


def create_tribe():
    """
    建图，将部落B的数据重新映并保存到部落A之后作为一整个list，图采用邻接表
    """
    global Asize, Bsize
    test_data = None
    with open(test_data_name, "r") as test_data_file:
        test_data_file_reader = csv.reader(test_data_file)
        test_data = list(test_data_file_reader)
    Asize = len(test_data)
    Bsize = len(test_data[0])

    for i in range(Asize):  # 预先申请部落A
        tribe.append([])
    for i in range(Bsize):  # 预先申请部落B
        tribe.append([])
    for i, raw in enumerate(test_data):
        for j, value in enumerate(raw):
            if value == '1':
                tribe[i].append(j + Asize)
                tribe[j + Asize].append(i)

    # print(len(tribe[:Asize]))
    # print(len(tribe[Asize:]))


def find_circle(start, depth, end_as_key):
    """
    start:int 起点id
    depth:int 当前搜索深度
    end_as_key:dict(int,list(list)) 以每条路径的最后一个id作为key,最后一个id相同的路径为value
    找环，每一次递归将之前的长度为n路径，延长为长度为n+1的路径并存入end_as_key_plus然后调用make_up_circle方法组合
    """
    end_as_key_plus = dict()
    for traces_of_some_end in end_as_key.values():
        for trace in traces_of_some_end:
            for nextid in tribe[trace[-1]]:
                if nextid <= start or nextid in trace:
                    continue
                if nextid in end_as_key_plus:
                    end_as_key_plus[nextid].append(trace + [nextid])
                else:
                    end_as_key_plus[nextid] = [trace + [nextid]]
    print(end_as_key_plus)
    make_up_circle(end_as_key_plus, depth)  # 根据新生成的长度为n+1的路径构造出长度为2n的环
    if depth >= MAX_LENGTH // 2 + 1:
        return
    find_circle(start, depth + 1, end_as_key_plus)


def make_up_circle(end_as_key, length):
    """
    end_as_key:dict(int,list(list)) 以每条路径的最后一个id作为key,最后一个id相同的路径为value
    length:int dict中路径的长度
    将找到的路径中首尾相同的两两匹配构造出最长的环，
    为避免无意义匹配，每条路径只会和排在其后面的路径匹配
    """
    circleSet = set()
    circleCountIndex = length - 3
    for traces_of_one_key in end_as_key.values():
        for trace_index, half_trace in enumerate(traces_of_one_key[:-1]):
            except_first_and_last_id_half_trace = half_trace[:-1]
            half_trace_set = set(except_first_and_last_id_half_trace)
            for other_half_trace in traces_of_one_key[trace_index + 1:]:
                for Id in other_half_trace[:-1]:  # 检查set中是否已经有除去首尾值的other_half_trace的id
                    if Id in half_trace_set:
                        break
                else:  # 中间没有重复值
                    newCircle = tuple(sorted(except_first_and_last_id_half_trace + other_half_trace))
                    circleSet.add(newCircle)
    circleCounts[circleCountIndex] = circleCounts[circleCountIndex] + len(circleSet)


def prepare_trace_length2(start, end_as_key):
    """
    start:int
    end_as_key:dict(int,list(list))
    此函数初始化出长度为2的路径集,
    起点都是一样的所以不用考虑
    """
    for nextid in tribe[start]:
        if nextid <= start:
            continue
        if nextid in end_as_key:
            end_as_key[nextid].append([nextid])
        else:
            end_as_key[nextid] = [[nextid]]


def find():
    """
    从部落A中选取每一个点作为起点开始搜索
    """
    for start in range(1):
        if len(tribe[start]) > 1:  # 只有一个度的点不可能构成环
            end_as_key = dict()
            prepare_trace_length2(start, end_as_key)
            print(end_as_key)
            find_circle(start, 3, end_as_key)


def output_result():
    with open(result_file_name, "w") as result_file:
        for count in circleCounts:
            result_file.write(str(count) + "\n")


if __name__ == '__main__':
    time_start = time.time()
    create_tribe()
    find()
    # output_result()

    # for circleCount in circleCounts:
    #     print(circleCount)
    #
    time_end = time.time()
    # print('totally cost', time_end - time_start, "s")


