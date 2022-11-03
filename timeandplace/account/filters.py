import django_filters
from .models import Profile

class ProfileFilter(django_filters.FilterSet):
  age_preference = django_filters.AllValuesFilter()

  class Meta:
      model = Profile
      fields = ['age_preference']