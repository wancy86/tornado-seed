# from forms.form import Form
# from forms import validators
# from common.decrators import authenticated, handle_request_exception
# from common.request import BaseHandler, JsonResponse

# class StudyHandler(BaseHandler):

#     class StudyForm(Form):
#         first_name = validators.String(min_value=1, max_value=50)
#         last_name = validators.String(min_value=1, max_value=50)

#     @handle_request_exception    
#     def get(self):
#         data = {
#             'first_name':'Miles', 
#             'last_name':'Yao'
#         }
        
#         return JsonResponse(self, '50000', msg='get request is invoked', data=data)

#     @handle_request_exception    
#     def post(self):
#         form = _Study.StudyForm(**self.POST)  
#         return JsonResponse(self, '50000', msg='post request is invoked', data=form.data)      

#     @handle_request_exception    
#     def delete(self):
#         return JsonResponse(self, '50000', msg='delete request is invoked')               

