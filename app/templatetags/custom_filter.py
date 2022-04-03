from django import template


register = template.Library()

# this filter is for getting total passenger by addding number of adult and child
# @register.filter(name="likeUnlike")
# def likeUnlike(like, feedback):
    
#     print(1)
#     print(like)
#     print(feedback)
#     if like == feedback:
#         return 5                                            