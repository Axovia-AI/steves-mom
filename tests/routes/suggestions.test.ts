import { generateUUID } from '@/lib/utils';
import { expect, test } from '../fixtures';
import { getMessageByErrorCode } from '@/lib/errors';

test.describe('/api/suggestions', () => {
  test('Ada cannot get suggestions without specifying a documentId', async ({
    adaContext,
  }) => {
    const response = await adaContext.request.get('/api/suggestions');
    expect(response.status()).toBe(400);

    const { code, message } = await response.json();
    expect(code).toEqual('bad_request:api');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Ada gets empty array for document with no suggestions', async ({
    adaContext,
  }) => {
    const documentId = generateUUID();

    const response = await adaContext.request.get(
      `/api/suggestions?documentId=${documentId}`,
    );
    expect(response.status()).toBe(200);

    const suggestions = await response.json();
    expect(suggestions).toEqual([]);
  });
});
