N=int(intput())
w=list(map(int,input().split()))
s=sum(w)
print((N-1)*( (s//N-1))) if s%N==0 else print(-1)