@authenticated
def put(self):
    form = [model_name].Form(**self.BODY)
    model = self.db.query([model_name]).filter([pk_filter]).first()   
    model.update(**form.data)           
    self.db.commit()
    return JsonResponse(self, '000')