import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FasterRunner.settings")  # project_name 项目名称
django.setup()

import time
from fastrunner import models


def time_cmp(first_time, second_time):
    """
    time
    """
    return int(time.strftime("%Y-%m-%d %H:%M:%S", first_time))


if __name__ == '__main__':
    # import time
    #
    #
    # def sumOfN3(n):
    #     start = time.time()
    #     c = (n * (n + 1)) / 2
    #     end = time.time()
    #     return c, end-start
    #
    # def sumOfN(n):
    #     start = time.time()
    #     theSum = 0
    #     for i in range(1, n + 1):
    #         theSum = theSum + i
    #     end = time.time()
    #     return theSum, end - start
    #
    #
    #
    # print("Sum	is	%d	required	%10.7f	seconds" % sumOfN(100000))
    # print("Sum	is	%d	required	%10.7f	seconds" % sumOfN3(100000))

    print(models.FileBinary.objects.get(id=12).body)

