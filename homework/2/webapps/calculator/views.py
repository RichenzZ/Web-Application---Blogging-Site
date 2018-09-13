from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def calculate(request):
	# context = {}
	reset_state = {"display": 0, "preval": 0, "op": "", "message":"Something is Wrong, the app is reset"}
	try:
		if request.POST:
			if 'digit' in request.POST:
				num = request.POST['digit']			
				prev_op = request.POST['prev_op']
				preval = request.POST.get('pre_val',"0")
				disval = request.POST.get('display',"0")
				# print("add digit")
				# print("preval = ", preval, "disval=", disval)
				if not preval:
					return render(request, 'calc_temp.html', {"display": disval + num, "preval": preval, "op": prev_op})
				if not disval or int(disval) == int(preval):
					return render(request, 'calc_temp.html', {"display": num, "preval": preval, "op": prev_op})
				return render(request, 'calc_temp.html', {"display": disval + num, "preval": preval, "op": prev_op})
			elif 'operator' in request.POST:
				prev_op = request.POST['prev_op']
				cur_op = request.POST['operator']
				disval = request.POST['display']
				preval = request.POST['pre_val']
				if not prev_op: 
				# no operation, separate the previous number, continue
					return render(request, 'calc_temp.html', {"display": disval, "preval": disval,"op": cur_op})
				# print("operation, prev_op=", prev_op, "preval = ", preval)
				if "+" in prev_op:
					result = int(preval) + int(disval)
				elif "-" in prev_op:
					result = int(preval) - int(disval)
				elif "*" in prev_op:
					result = int(preval) * int(disval)
				elif "/" in prev_op:
					if int(disval) == 0:
						return render(request, 'calc_temp.html',reset_state)
					result = int(int(preval) / int(disval))
				if '=' in cur_op:
					return render(request, 'calc_temp.html', {"display": str(result), "preval":str(result),"op": ""})
				return render(request, 'calc_temp.html', {"display": str(result), "preval":str(result), "op":cur_op})
			return render(request, 'calc_temp.html',reset_state)
	except:
		print("reset")
		return render(request, 'calc_temp.html',reset_state)
	return render(request, 'calc_temp.html',{})

	



