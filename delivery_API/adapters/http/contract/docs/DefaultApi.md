# OpenApi.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_courier**](DefaultApi.md#create_courier) | **POST** /api/v1/couriers | Добавить курьера
[**create_order**](DefaultApi.md#create_order) | **POST** /api/v1/orders | Создать заказ
[**get_couriers**](DefaultApi.md#get_couriers) | **GET** /api/v1/couriers | Получить всех курьеров
[**get_orders**](DefaultApi.md#get_orders) | **GET** /api/v1/orders/active | Получить все незавершенные заказы


# **create_courier**
> create_courier(new_courier=new_courier)

Добавить курьера

Позволяет добавить курьера

### Example


```python
import OpenApi
from OpenApi.models.new_courier import NewCourier
from OpenApi.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = OpenApi.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with OpenApi.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = OpenApi.DefaultApi(api_client)
    new_courier = OpenApi.NewCourier() # NewCourier | Курьер (optional)

    try:
        # Добавить курьера
        api_instance.create_courier(new_courier=new_courier)
    except Exception as e:
        print("Exception when calling DefaultApi->create_courier: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **new_courier** | [**NewCourier**](NewCourier.md)| Курьер | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Успешный ответ |  -  |
**400** | Ошибка валидации |  -  |
**409** | Ошибка выполнения бизнес логики |  -  |
**0** | Ошибка |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_order**
> create_order()

Создать заказ

Позволяет создать заказ с целью тестирования

### Example


```python
import OpenApi
from OpenApi.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = OpenApi.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with OpenApi.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = OpenApi.DefaultApi(api_client)

    try:
        # Создать заказ
        api_instance.create_order()
    except Exception as e:
        print("Exception when calling DefaultApi->create_order: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Успешный ответ |  -  |
**0** | Ошибка |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_couriers**
> List[Courier] get_couriers()

Получить всех курьеров

Позволяет получить всех курьеров

### Example


```python
import OpenApi
from OpenApi.models.courier import Courier
from OpenApi.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = OpenApi.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with OpenApi.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = OpenApi.DefaultApi(api_client)

    try:
        # Получить всех курьеров
        api_response = api_instance.get_couriers()
        print("The response of DefaultApi->get_couriers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_couriers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Courier]**](Courier.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Успешный ответ |  -  |
**0** | Ошибка |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orders**
> List[Order] get_orders()

Получить все незавершенные заказы

Позволяет получить все незавершенные заказы

### Example


```python
import OpenApi
from OpenApi.models.order import Order
from OpenApi.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = OpenApi.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with OpenApi.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = OpenApi.DefaultApi(api_client)

    try:
        # Получить все незавершенные заказы
        api_response = api_instance.get_orders()
        print("The response of DefaultApi->get_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_orders: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Order]**](Order.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Успешный ответ |  -  |
**0** | Ошибка |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

