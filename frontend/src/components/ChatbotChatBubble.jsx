import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ChatbotChatBubble({key, value, loading}) {
  return(
    <>
      <div className={`w-3/4 h-auto p-2 rounded-[20px] break-words min-w-0 ${loading ? 'text-gray-500 animate-[pulse_1.5s_ease-in-out_infinite]' : 'text-[var(--color-text)]'}`} key={key}>
          <div className='
        text-base
        [&>*+*]:mt-4

        [&_h1]:text-2xl [&_h1]:font-bold [&_h1]:mt-6 [&_h1]:mb-3
        [&_h2]:text-xl [&_h2]:font-bold [&_h2]:mt-6 [&_h2]:mb-3
        [&_h3]:text-lg [&_h3]:font-semibold [&_h3]:mt-5 [&_h3]:mb-2

        [&_p]:leading-7

        [&_ul]:pl-6
        [&_ol]:list-decimal [&_ol]:pl-6
        [&_li]:pl-1 [&_li]:mt-2

        [&_table]:w-full [&_table]:border-collapse [&_table]:my-5
        [&_th]:border [&_th]:p-3 [&_th]:text-left
        [&_td]:border [&_td]:p-3 [&_td]:align-top

        [&_blockquote]:border-l-4
        [&_blockquote]:border-gray-400
        [&_blockquote]:pl-4 [&_blockquote]:my-4

        [&_pre]:p-4 [&_pre]:rounded-xl
        [&_pre]:bg-[#15161A] [&_pre]:text-white
        [&_pre]:overflow-x-auto [&_pre]:my-4
        [&_code]:font-mono
        [&_code]:text-sm

        [&_hr]:my-6

        [&_a]:text-blue-500 [&_a]:underline
        [&_strong]:font-bold

        overflow-x-auto
          '>
            <Markdown remarkPlugins={[remarkGfm]}>
              {value}
            </Markdown>
        </div>
      </div>
    </>
  )
}

 