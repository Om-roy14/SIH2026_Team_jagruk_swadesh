import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

/**
 * MarkdownRenderer
 * Renders markdown from the RAG pipeline with Jagruk Swadesh dark-theme styling.
 * Supports: headings, bold/italic, lists, tables (GFM), code, blockquotes, <hr>.
 */
export default function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        // ── Headings ──────────────────────────────────────────────────────────
        h1: ({ children }) => (
          <h1 className="text-base font-black text-saffron tracking-tight mt-4 mb-2 first:mt-0">
            {children}
          </h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-sm font-extrabold text-amber-300 tracking-tight mt-4 mb-2 first:mt-0 border-b border-white/10 pb-1">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-sm font-bold text-white/90 mt-3 mb-1.5">
            {children}
          </h3>
        ),
        h4: ({ children }) => (
          <h4 className="text-xs font-bold text-ivory uppercase tracking-wider mt-3 mb-1">
            {children}
          </h4>
        ),

        // ── Paragraph ─────────────────────────────────────────────────────────
        p: ({ children }) => (
          <p className="text-ivory leading-relaxed mb-2 last:mb-0">
            {children}
          </p>
        ),

        // ── Bold & Italic ─────────────────────────────────────────────────────
        strong: ({ children }) => (
          <strong className="font-bold text-white">{children}</strong>
        ),
        em: ({ children }) => (
          <em className="italic text-ivory-dim">{children}</em>
        ),

        // ── Unordered list ────────────────────────────────────────────────────
        ul: ({ children }) => (
          <ul className="space-y-1 my-2 pl-1">{children}</ul>
        ),
        // Ordered list
        ol: ({ children }) => (
          <ol className="space-y-1 my-2 pl-1 list-decimal list-inside">{children}</ol>
        ),
        li: ({ children, ordered }) => (
          <li className="flex items-start gap-2 text-ivory text-xs sm:text-sm leading-relaxed">
            {!ordered && (
              <span className="text-saffron font-bold mt-0.5 shrink-0">•</span>
            )}
            <span>{children}</span>
          </li>
        ),

        // ── Table (GFM) ───────────────────────────────────────────────────────
        table: ({ children }) => (
          <div className="overflow-x-auto my-3 rounded-xl border border-white/10">
            <table className="w-full text-xs sm:text-sm border-collapse">
              {children}
            </table>
          </div>
        ),
        thead: ({ children }) => (
          <thead className="bg-saffron/20 text-saffron font-bold text-left">
            {children}
          </thead>
        ),
        tbody: ({ children }) => (
          <tbody className="divide-y divide-white/10">{children}</tbody>
        ),
        tr: ({ children }) => (
          <tr className="hover:bg-white/5 transition-colors">{children}</tr>
        ),
        th: ({ children }) => (
          <th className="px-3 py-2 font-extrabold text-saffron text-[11px] uppercase tracking-wider whitespace-nowrap">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="px-3 py-2 text-ivory align-top">{children}</td>
        ),

        // ── Code ─────────────────────────────────────────────────────────────
        code: ({ inline, children }) =>
          inline ? (
            <code className="px-1.5 py-0.5 rounded bg-white/10 text-amber-300 font-mono text-[11px]">
              {children}
            </code>
          ) : (
            <pre className="my-3 p-3 rounded-xl bg-black/40 border border-white/10 overflow-x-auto">
              <code className="font-mono text-[11px] text-emerald-300 leading-relaxed">
                {children}
              </code>
            </pre>
          ),

        // ── Blockquote ────────────────────────────────────────────────────────
        blockquote: ({ children }) => (
          <blockquote className="my-2 pl-3 border-l-2 border-saffron/60 text-ivory-dim italic">
            {children}
          </blockquote>
        ),

        // ── Horizontal rule ───────────────────────────────────────────────────
        hr: () => <hr className="my-3 border-white/10" />,

        // ── Links ─────────────────────────────────────────────────────────────
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-amber-300 underline underline-offset-2 hover:text-white transition-colors"
          >
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
