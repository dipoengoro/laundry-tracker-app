import {ref} from 'vue';
import {useApi} from './useApi';
import axios from 'axios';


export function usePresignedUrl() {
    const {api} = useApi();
    const presignedUrl = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const getPresignedUrl = async (clothingId, file) => {
        loading.value = true;
        error.value = null;

        const uploadData = await getUploadUrl(clothingId, file)

        if (!uploadData || !uploadData.url) {
            loading.value = false;
            error.value = 'Failed to get upload URL.'
            return false
        }

        try {
            await axios.put(uploadData.url, file, {
                headers: {
                    'Content-Type': file.type
                }
            });

            loading.value = false;
            return true;
        } catch (err) {
            error.value = 'File upload failed';
            console.error('Failed to get presigned URL', err);
            loading.value = false;
        }
    };

    const uploadFile = async (clothingId, file) => {
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
