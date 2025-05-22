# Courier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Идентификатор | 
**name** | **str** | Имя | 
**location** | [**Location**](Location.md) |  | 

## Example

```python
from OpenApi.models.courier import Courier

# TODO update the JSON string below
json = "{}"
# create an instance of Courier from a JSON string
courier_instance = Courier.from_json(json)
# print the JSON string representation of the object
print(Courier.to_json())

# convert the object into a dict
courier_dict = courier_instance.to_dict()
# create an instance of Courier from a dict
courier_from_dict = Courier.from_dict(courier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


