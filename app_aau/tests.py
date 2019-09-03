class ConditionalBMR(models.Model):
    bmr = models.ForeignKey(, on_delete=models.CASCADE)
    conditional_rate = models.IntegerField()
    conditional_rate_start_date = models.DateField(null = True)
    conditional_rate_end_date =  models.DateField(null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bmr

class OrderTemplateData(models.Model):
    order_template_name = models.CharField(max_length=255)
    lane =  models.ForeignKey(, on_delete=models.CASCADE)
    shipper =  models.ForeignKey(, on_delete=models.CASCADE)
    Vechile_type_id =  models.ForeignKey(, on_delete=models.CASCADE)
    no_of_vehicles = models.IntegerField()
    commodity = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    consignee_name = models.CharField(max_length=255)
    consignee_email = models.EmailField(max_length=255)
    consignee_phone = models.IntegerField()
    consignee_country = models.CharField(max_length=255)
    remark = models.TextField()

class Trip(models.Model):

    order_id = models.ForeignKey(, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(, on_delete=models.CASCADE)
    trip_json = models.TextField()

class TripLog(models.Model):
    trip_id = models.ForeignKey(, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null = True)
    content_details = models.TextField()
    trip_additional_charges = models.TextField()

class Contract(models.Model):

    lane_id = models.ForeignKey(, on_delete=models.CASCADE)
    shipper_id = models.ForeignKey(, on_delete=models.CASCADE)
    transporter_id = models.ForeignKey(, on_delete=models.CASCADE)
    rate = models.FloatField()
    status =
    shipper_remarks = models.TextField()
    admin_remarks = models.TextField()
    contract_issue_date = models.DateTimeField(null = True)
    contract_expiry_date = models.DateTimeField(null = True)
    is_lease = models.BooleanField(default=False)
    is_trip = models.BooleanField(default=False)

    default_service_type = 'Domestic'
    Service_type_Choices = [
        (default_service_type, 'Domestic'),
        ('Cross Border', 'Cross Border'),
        ('Containerized', 'Containerized'),
    ]
    service_type  = models.CharField(
        max_length=100,
        choices=Service_type_Choices,
        default=default_service_type,
    )
