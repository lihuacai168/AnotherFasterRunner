import * as React from 'react';
export interface IEllipsisProps {
  tooltip?: boolean;
  length?: number;
  lines?: number;
  style?: React.CSSProperties;
  className?: string;
  fullWidthRecognition?: boolean;
}

export default class Ellipsis extends React.Component<IEllipsisProps, any> {}
