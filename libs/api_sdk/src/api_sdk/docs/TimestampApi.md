# api_sdk.TimestampApi

All URIs are relative to *https://helloacm.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_timestamp**](TimestampApi.md#convert_timestamp) | **GET** /api/unix-timestamp-converter/ | Convert Unix timestamp or date-time string


# **convert_timestamp**
> ConvertTimestamp200Response convert_timestamp(cached=cached, s=s)

Convert Unix timestamp or date-time string

### Example


```python
import api_sdk
from api_sdk.models.convert_timestamp200_response import ConvertTimestamp200Response
from api_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://helloacm.com
# See configuration.py for a list of all supported configuration parameters.
configuration = api_sdk.Configuration(
    host = "https://helloacm.com"
)


# Enter a context with an instance of the API client
with api_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_sdk.TimestampApi(api_client)
    cached = 'cached_example' # str | Enable caching for the conversion (optional)
    s = api_sdk.ConvertTimestampSParameter() # ConvertTimestampSParameter | The Unix timestamp (integer) or date string (YYYY-MM-DD HH:MM:SS) to convert (optional)

    try:
        # Convert Unix timestamp or date-time string
        api_response = api_instance.convert_timestamp(cached=cached, s=s)
        print("The response of TimestampApi->convert_timestamp:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TimestampApi->convert_timestamp: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cached** | **str**| Enable caching for the conversion | [optional] 
 **s** | [**ConvertTimestampSParameter**](.md)| The Unix timestamp (integer) or date string (YYYY-MM-DD HH:MM:SS) to convert | [optional] 

### Return type

[**ConvertTimestamp200Response**](ConvertTimestamp200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversion result. On success, returns a timestamp object or human-readable date time. On invalid input, returns false |  -  |
**404** | Invalid query format or missing query parameters |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

