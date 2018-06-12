@authenticated
def get(self):
    ACTION = self.GET['ACTION']
    if ACTION == 'ONE':
        model = self.db.query([model_name]).filter([pk_filter]).first()  
        return JsonResponse(self, '000', data=model.json) 
    elif ACTION == 'QUERY':
        data = [item.json for item in self.db.query([model_name]).all()] 
        return JsonResponse(self, '000', data=data) 
    else:
    	pass