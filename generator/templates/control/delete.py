@authenticated
def delete(self):
    model = self.db.query([model_name]).filter([delete_filter]).first()
    self.db.delete(model)
    self.db.commit()
    return JsonResponse(self, '000')   