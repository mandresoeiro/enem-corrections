class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "bio",
            "course",  # substituído school → course
            "grade",
            "total_essays",
            "created_at",
        ]
