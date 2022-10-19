import * as React from 'react';
import {Divider, message, Row} from 'antd';
import { injectIntl } from 'react-intl';
import CopyableIcon from './CopyableIcon';
import { ThemeType } from './index';
import { CategoriesKeys } from './fields';

interface CategoryProps {
  title: CategoriesKeys;
  icons: string[];
  theme: ThemeType;
  newIcons: string[];
  intl: any;
}

interface CategoryState {
  justCopied: string | null;
}

class Category extends React.Component<CategoryProps, CategoryState> {
  copyId?: number;

  state = {
    justCopied: null,
  };

  componentWillUnmount() {
    window.clearTimeout(this.copyId);
  }

  onCopied = (type: string, text: string) => {
    message.success(
      <span>
        <code className="copied-code">{text}</code> copied 🎉
      </span>,
    );
    this.setState({ justCopied: type }, () => {
      this.copyId = window.setTimeout(() => {
        this.setState({ justCopied: null });
      }, 2000);
    });
  };

  render() {
    const {
      icons,
      title,
      newIcons,
      theme,
      intl: { messages },
      setCurrentIcon,
      currentIcon,
      closeIcon
    } = this.props;
    const items = icons.map(name => {
      return (
        <CopyableIcon
            setCurrentIcon={setCurrentIcon}
            currentIcon={currentIcon}
          key={name}
          name={name}
          theme={theme}
          isNew={newIcons.indexOf(name) >= 0}
          justCopied={this.state.justCopied}
          onCopied={this.onCopied}
            closeIcon={closeIcon}
        />
      );
    });

    return (
      <div style={{paddingTop: 5, width: '100%'}}>
        <h3>{messages[`app.docs.components.icon.category.${title}`]}</h3>
        <ul className="anticons-list">
          <Row>
            {items}
          </Row>
        </ul>
        <Divider style={{margin: 5}}/>
      </div>
    );
  }
}

export default injectIntl(Category);
