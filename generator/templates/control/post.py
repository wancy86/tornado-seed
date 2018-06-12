@authenticated
def post(self):
    form = [model_name].Form(**self.BODY)  
    model = [model_name](**form.data)
    self.db.add(model)
    self.db.commit()
    return JsonResponse(self, '000', data=model.json)  