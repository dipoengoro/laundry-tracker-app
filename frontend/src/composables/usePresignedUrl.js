import {ref} from 'vue';
import {useApi} from './useApi';

export function usePresignedUrl() {
    const {api} = useApi();
    const presignedUrl = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const getPresignedUrl = async (clothingId, file) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await api.post(`/clothing/${clothingId}/image-upload-url`, {
                file_name: file.name,
                content_type: file.type,
            });
            presignedUrl.value = response.data;
            return response.data;
        } catch (err) {
            error.value = err;
            console.error('Failed to get presigned URL', err);
        } finally {
            loading.value = false;
        }
    };

    const uploadFile = async (presignedUrlData, file) => {
        loading.value = true;
        error.value = null;
        try {
            const formData = new FormData();
            Object.entries(presignedUrlData.fields).forEach(([key, value]) => {
                formData.append(key, value);
            });
            formData.append('file', file);

            const response = await fetch(presignedUrlData.url, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('File upload failed');
            }

            return response;
        } catch (err) {
            error.value = err;
            console.error('Failed to upload file', err);
        } finally {
            loading.value = false;
        }
    };

    return {
        presignedUrl,
        loading,
        error,
        getPresignedUrl,
        uploadFile,
    };
}
