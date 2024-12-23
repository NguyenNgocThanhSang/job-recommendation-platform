import { getRequest, postRequest } from '@/lib/fetch';

export const useUser = () => {
  const onGetAvatar = async (callback) => {
    try {
      const response = await getRequest({
        endPoint: '/user/avatar/',
      });
      console.log('🚀 ~ onGetAvatar ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  const onPostCv = async (data, callback) => {
    try {
      const response = await postRequest({
        endPoint: '/user/cv/',
        formData: data,
        isFormData: true,
      });
      console.log('🚀 ~ onPostCv ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  const onGetCv = async (callback) => {
    try {
      const response = await getRequest({
        endPoint: '/user/cv/',
      });
      console.log('🚀 ~ onGetCv ~ response:', response);
      callback(response.data.data);
    } catch (error) {
      callback(error);
    }
  };
  return {
    onGetAvatar,
    onPostCv,
    onGetCv,
  };
};
