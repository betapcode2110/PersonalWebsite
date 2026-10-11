import { visit } from 'unist-util-visit';

export function rehypeImageCaption() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      // Case 1: <p><img/video title="..." /></p>
      if (node.tagName === 'p' && node.children.length === 1) {
        const child = node.children[0];
        if (child && child.type === 'element' && (child.tagName === 'img' || child.tagName === 'video') && child.properties?.title) {
          const title = String(child.properties.title).trim();
          if (title) {
            node.tagName = 'figure';
            node.properties = {
              className: ['media-figure', 'my-6', 'flex', 'flex-col', 'items-center']
            };
            node.children = [
              child,
              {
                type: 'element',
                tagName: 'figcaption',
                properties: {
                  className: ['text-center', 'text-xs', 'sm:text-sm', 'text-[#6b7280]', 'mt-2', 'italic']
                },
                children: [{ type: 'text', value: title }]
              }
            ];
            return;
          }
        }
      }

      // Case 2: Standalone <img title="..." /> or <video title="..." /> where parent is not figure or p
      if (node && (node.tagName === 'img' || node.tagName === 'video') && node.properties?.title && parent && parent.tagName !== 'figure' && parent.tagName !== 'p') {
        const title = String(node.properties.title).trim();
        if (title && typeof index === 'number') {
          const figure = {
            type: 'element',
            tagName: 'figure',
            properties: {
              className: ['media-figure', 'my-6', 'flex', 'flex-col', 'items-center']
            },
            children: [
              node,
              {
                type: 'element',
                tagName: 'figcaption',
                properties: {
                  className: ['text-center', 'text-xs', 'sm:text-sm', 'text-[#6b7280]', 'mt-2', 'italic']
                },
                children: [{ type: 'text', value: title }]
              }
            ]
          };
          parent.children.splice(index, 1, figure);
        }
      }
    });
  };
}
