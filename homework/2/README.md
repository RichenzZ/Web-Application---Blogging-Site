Reason for choose POST request: post method allows the data sent to the server to be stored in the request body so that in the views.py we can fetch what we need for computing the result more easily. Besides, post method does not have its data shown in the url, which I think it is better get method in an application like calculator.

Some special inputs:
if user inputs operator consecutively, the calculator will compute the result by using the last result. 
eg: "result + +" will get result + result, "result - -" will get result - result

Invalid input:
when invalid inputs like divide by zero happen, the app will display message "Something is Wrong, the app is reset" and reset the app.


