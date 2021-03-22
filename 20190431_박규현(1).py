import numpy as np

con = "예"

while(con == "예"):
    row1, col1 = eval(input("행, 열 크기 입력 :"))
    row2, col2 = eval(input("행, 열 크기 입력 :"))

    mat1 = np.random.randint(1, 11, size = (row1, col1))
    mat2 = np.random.randint(1, 11, size = (row2, col2))

    print("첫 번째 행렬 : \n", mat1)
    print("두 번째 행렬 : \n", mat2)

    if (row1 == row2) and (col1 == col2):
        print("+ 연산 결과 : \n", mat1+mat2)

    elif (row1 == row2) and (col1 == 1 or col2 ==1):
        if col1 == 1:
            new_mat = [[mat1] for i in range(col2)]
            new_mat1 = new_mat + mat2
        
        else:
            new_mat = [[mat2] for i in range(col1)]
            new_mat1 = new_mat + mat1

        print("+ 연산 결과 : \n", new_mat1[0])
    
    elif (row1 == 1 or row2 == 1) and (col1 == col2):
        if row1 == 1:
            new_mat = [[mat1] for i in range(row2)]
            new_mat1 = new_mat + mat2
        
        else:
            new_mat = [[mat2] for i in range(row1)]
            new_mat1 = new_mat + mat1

        print("+ 연산 결과 : \n", new_mat1[0])

    elif (row1 == col2 and row2 == col1) and (row1 == 1 or col1 == 1):
        if row1 == 1:
            new_mat = np.array([[mat1] for i in range(row2)])
            new_mat1 = np.array([[mat2] for i in range(col1)])
            new_mat3 = new_mat + new_mat1

        else:
            new_mat = np.array([[mat1] for i in range(row1)])
            new_mat1 = np.array([[mat2] for i in range(col2)])
            new_mat3 = new_mat + new_mat1
        
        print("+ 연산 결과 : \n", new_mat3[0])

    else:
        print("+ 연산이 불가능합니다.")

    if col1 == row2:
        new_mat2 = [[0 for i in range(row1)] for j in range(col2)]
        new_mat2 = mat1.dot(mat2)
        print("행렬 곱 연산 결과 : \n", new_mat2)

    else:
        print("행렬 곱 연산이 불가능합니다.")

    con = input(">>>>> 계속할까요? (예/아니오)")