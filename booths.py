from flask import Flask, render_template, request
from bitstring import BitArray

def booth(m,r):
	x = len(bin(m))
	y = len(bin(r))
	#after both numbers are negative, for some reason, the answer is one less than whats expected.
	if m<0 and r<0:
		bugbit=1
	else:
		bugbit = 0
	totalLength = x+y + 1
	mA = BitArray(int = m, length = totalLength)
	# what we do here is , BIT WISE left shift, toh we shift it by y+1 bits
	A = mA << (y+1)
	compliment = BitArray(int = -m, length = totalLength) << (y+1) # again we just take the array, and left shift it also, this is the 2s compliment of m we take
	P = BitArray(int = r, length = totalLength)
	P = P << 1  # end mein ek 0 dala as the value of "Q ' "
	for i in range(1,y+1):
		if P[-2:] == '0b01': #last two check kia
			P = BitArray(int = P.int + A.int, length = totalLength) # 0 1 ? 0+1
		elif P[-2:] == '0b10':
			P = BitArray(int = P.int +compliment.int, length = totalLength) #  1 0 ? 1-0 (S has two's compliment )
		P = BitArray(int=P.int >> 1,length=totalLength) #shift
	P = P[:-1] #manditory shift if not shifted.
	P.int = P.int + bugbit
	return '<h1>RESULT</h1><br><h3>decimal value: '+str(P.int)+'</br><br> binary value: '+str(P.bin)

# flask starts here

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/', methods = ['POST'])
# 3 general methods: post, get , put. We use post to get whats there in tabs
def my_form_post():
	multiplicand = request.form['Multiplicand']
	multiplier = request.form['Multiplier']
	try:
		multiplicand = int(multiplicand)
		multiplier = int(multiplier)
	except:
		return "<h1>ERROR</h1><br>Only one item for multiplication of two found"

	return booth(multiplicand, multiplier)

if __name__ == '__main__':
    app.debug = True
    app.run()
