'use client';

import { useChat } from '@/hooks/useChat';
import { PromptSuggestions } from '@/lib/constants';
import { cn } from '@/lib/utils';
import { Button } from '@nextui-org/react';

import { useMutation } from '@tanstack/react-query';
import { CornerDownLeft, Loader2 } from 'lucide-react';
import { nanoid } from 'nanoid';
import { FC, HTMLAttributes, useContext, useRef, useState } from 'react';
import { toast } from 'react-hot-toast';
import TextareaAutosize from 'react-textarea-autosize';

interface ChatInputProps extends HTMLAttributes<HTMLDivElement> {
  selectedJob: any;
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  isMessageUpdating: boolean;
  setIsMessageUpdating: (isUpdating: boolean) => void;
}

const ChatInput: FC<ChatInputProps> = ({
  className,
  selectedJob,
  messages,
  setMessages,
  isMessageUpdating,
  setIsMessageUpdating,
  ...props
}) => {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const [input, setInput] = useState<string>('');

  const { onPostChat } = useChat();

  const { mutate: sendMessage, isLoading } = useMutation({
    mutationKey: ['sendMessage'],
    // include message to later use it in onMutate
    mutationFn: async (inputText: string) => {
      const response = await onPostChat({
        job_id: selectedJob.id,
        message: inputText,
      });
      console.log('🚀 ~ onPostChat ~ response:', response);
      const responseMessage = {
        id: nanoid(),
        isUserMessage: false,
        message: response.message,
        jobId: selectedJob.id,
      };
      setMessages([...messages, responseMessage]);
      return responseMessage;
    },
    onMutate: (inputText: string) => {
      setIsMessageUpdating(true);
      const message: Message = {
        id: nanoid(),
        isUserMessage: true,
        message: inputText,
        jobId: selectedJob.id,
      };
      setMessages([...messages, message]);
      setInput('');
    },
    onSuccess: async (stream) => {
      if (!stream) throw new Error('No stream');

      setIsMessageUpdating(false);

      setInput('');

      setTimeout(() => {
        textareaRef.current?.focus();
      }, 10);
    },
    onError: (_, inputText) => {
      toast.error('Something went wrong. Please try again.');
      const message: Message = {
        id: nanoid(),
        isUserMessage: true,
        message: inputText,
        jobId: selectedJob.id,
      };
      setMessages(messages.filter((msg) => msg.id !== message.id));
      textareaRef.current?.focus();
    },
  });

  // Helper function to shuffle an array of suggestions
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
  const randomSuggestions = shuffleArray([...PromptSuggestions]).slice(0, 2);

  return (
    <div
      {...props}
      className={cn((className = `flex flex-col px-2 pb-3 gap-3`))}
    >
      <div className="w-full flex flex-row justify-start gap-3">
        {!isMessageUpdating &&
          randomSuggestions.map((suggestion) => (
            <Button
              variant="bordered"
              key={suggestion}
              onClick={() => {
                sendMessage(suggestion);
              }}
              className="text-xs text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-0"
            >
              {suggestion}
            </Button>
          ))}
      </div>

      <div className="relative w-full lex-1 overflow-hidden rounded-lg border-none outline-none">
        <TextareaAutosize
          ref={textareaRef}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();

              if (input !== '') {
                const inputText = input.trim();
                sendMessage(inputText);
              }
            }
          }}
          rows={2}
          maxRows={4}
          value={input}
          disabled={isLoading}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Write a message..."
          className="peer disabled:opacity-50 pr-14 resize-none block w-full border-0 bg-zinc-100 py-1.5 text-gray-900 focus:ring-0 text-sm sm:leading-6"
        />

        <div className="absolute inset-y-0 right-0 flex py-1.5 pr-1.5">
          <kbd className="inline-flex items-center rounded border bg-white border-gray-200 px-1 font-sans text-xs text-gray-400">
            {isLoading ? (
              <Loader2 className="w-3 h-3 animate-spin" />
            ) : (
              <CornerDownLeft className="w-3 h-3" />
            )}
          </kbd>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
