import { generateUUID } from '@/lib/utils';
import { expect, test } from '../fixtures';
import { getMessageByErrorCode } from '@/lib/errors';

const chatIdsCreatedByAda: Array<string> = [];
const messageIdsCreatedByAda: Array<string> = [];

test.describe.serial('/api/vote', () => {
  test.beforeAll(async ({ adaContext }) => {
    // Create a chat first
    const chatId = generateUUID();
    const messageId = generateUUID();

    const response = await adaContext.request.post('/api/chat', {
      data: {
        id: chatId,
        message: {
          id: messageId,
          role: 'user',
          parts: [{ type: 'text', text: 'Why is the sky blue?' }],
          createdAt: new Date().toISOString(),
        },
        selectedChatModel: 'chat-model',
        selectedVisibilityType: 'private',
      },
    });

    expect(response.status()).toBe(200);
    chatIdsCreatedByAda.push(chatId);
    messageIdsCreatedByAda.push(messageId);

    // Wait for response to complete
    await response.body();
  });

  test('Ada cannot get votes without specifying a chatId', async ({
    adaContext,
  }) => {
    const response = await adaContext.request.get('/api/vote');
    expect(response.status()).toBe(400);

    const { code, message } = await response.json();
    expect(code).toEqual('bad_request:api');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Ada cannot get votes for a non-existent chat', async ({
    adaContext,
  }) => {
    const fakeChatId = generateUUID();
    const response = await adaContext.request.get(
      `/api/vote?chatId=${fakeChatId}`,
    );
    expect(response.status()).toBe(404);

    const { code, message } = await response.json();
    expect(code).toEqual('not_found:chat');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Babbage cannot get votes for Ada\'s private chat', async ({
    babbageContext,
  }) => {
    const [chatId] = chatIdsCreatedByAda;

    const response = await babbageContext.request.get(
      `/api/vote?chatId=${chatId}`,
    );
    expect(response.status()).toBe(403);

    const { code, message } = await response.json();
    expect(code).toEqual('forbidden:vote');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Ada can get votes for her chat', async ({ adaContext }) => {
    const [chatId] = chatIdsCreatedByAda;

    const response = await adaContext.request.get(`/api/vote?chatId=${chatId}`);
    expect(response.status()).toBe(200);

    const votes = await response.json();
    expect(Array.isArray(votes)).toBe(true);
  });

  test('Ada cannot vote without required parameters', async ({
    adaContext,
  }) => {
    const response = await adaContext.request.patch('/api/vote', {
      data: {},
    });
    expect(response.status()).toBe(400);

    const { code, message } = await response.json();
    expect(code).toEqual('bad_request:api');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Ada cannot vote on a non-existent chat', async ({ adaContext }) => {
    const fakeChatId = generateUUID();
    const fakeMessageId = generateUUID();

    const response = await adaContext.request.patch('/api/vote', {
      data: {
        chatId: fakeChatId,
        messageId: fakeMessageId,
        type: 'up',
      },
    });
    expect(response.status()).toBe(404);

    const { code, message } = await response.json();
    expect(code).toEqual('not_found:chat');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Babbage cannot vote on Ada\'s chat', async ({ babbageContext }) => {
    const [chatId] = chatIdsCreatedByAda;
    const [messageId] = messageIdsCreatedByAda;

    const response = await babbageContext.request.patch('/api/vote', {
      data: {
        chatId,
        messageId,
        type: 'up',
      },
    });
    expect(response.status()).toBe(403);

    const { code, message } = await response.json();
    expect(code).toEqual('forbidden:vote');
    expect(message).toEqual(getMessageByErrorCode(code));
  });

  test('Ada can upvote a message', async ({ adaContext }) => {
    const [chatId] = chatIdsCreatedByAda;
    const [messageId] = messageIdsCreatedByAda;

    const response = await adaContext.request.patch('/api/vote', {
      data: {
        chatId,
        messageId,
        type: 'up',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Ada can downvote the same message (updates existing vote)', async ({
    adaContext,
  }) => {
    const [chatId] = chatIdsCreatedByAda;
    const [messageId] = messageIdsCreatedByAda;

    const response = await adaContext.request.patch('/api/vote', {
      data: {
        chatId,
        messageId,
        type: 'down',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Ada can verify vote was recorded', async ({ adaContext }) => {
    const [chatId] = chatIdsCreatedByAda;
    const [messageId] = messageIdsCreatedByAda;

    const response = await adaContext.request.get(`/api/vote?chatId=${chatId}`);
    expect(response.status()).toBe(200);

    const votes = await response.json();
    expect(votes.length).toBeGreaterThan(0);

    const vote = votes.find(
      (v: { messageId: string }) => v.messageId === messageId,
    );
    expect(vote).toBeDefined();
    expect(vote.isUpvoted).toBe(false); // We downvoted last
  });
});
