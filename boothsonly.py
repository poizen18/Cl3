from bitstring import BitArray

def booth(m,r):
	x=y=8
	totalLength = x+y + 1
	mA = BitArray(int = m, length = totalLength)
	rA = BitArray(int = r, length = totalLength)
	# what we do here is , BIT WISE left shift, toh we shift it by y+1 bits
	A = mA << (y+1)
	S = BitArray(int = -m, length = totalLength) << (y+1) # again we just take the array, and left shift it also, this is the 2s compliment of m we take
	P = BitArray(int = r, length = y)
	P.prepend(BitArray(int = 0, length = x)) # iske samne 8 bits laga diye
	P = P << 1  # end mein ek 0 dala as the value of "Q ' "
	for i in range(1,y+1):
		if P[-2:] == '0b01': #last two check kia
			P = BitArray(int = P.int + A.int, length = totalLength) # 0 1 ? 0+1
		elif P[-2:] == '0b10':
			P = BitArray(int = P.int +S.int, length = totalLength) #  1 0 ? 1-0 (S has two's compliment )
		P = arith_shift_right(P, 1)
	P = arith_shift_right(P, 1)
	return P.int

def arith_shift_right(x, amt):
	l = x.len
	x = BitArray(int = (x.int >> amt), length = l)
	return x


b = booth(86, 41)
print b