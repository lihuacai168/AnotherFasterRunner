import {
  Button,
  Table,
  Form,
  Tree,
  Container,
  Row,
  Col,
  Header,
  Main,
  Icon,
  Aside,
  Menu,
  Submenu,
  MenuItem,
  TableColumn,
  Switch,
  Popover,
  Image,
  Input,
  Pagination,
  Tabs,
  TabPane,
  RadioButton,
  Dialog,
  FormItem,
  RadioGroup,
  Select,
  Option,
  InputNumber,
  Tooltip,
  Badge,
  Checkbox,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  Autocomplete,
  Tag,
  Card,
  Drawer,
  Footer,
  Radio,
  Upload,
  Loading,
  Notification,
  MessageBox,
  Message
} from "element-ui";

const coms = [
  Button,
  Table,
  Form,
  Tree,
  Container,
  Row,
  Col,
  Header,
  Main,
  Icon,
  Aside,
  Menu,
  Submenu,
  MenuItem,
  TableColumn,
  Switch,
  Popover,
  Image,
  Input,
  Pagination,
  Tabs,
  TabPane,
  RadioButton,
  Dialog,
  FormItem,
  RadioGroup,
  Select,
  Option,
  InputNumber,
  Tooltip,
  Badge,
  Checkbox,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  Autocomplete,
  Tag,
  Card,
  Drawer,
  Footer,
  Radio,
  Upload
  // Loading
];

export default {
  install(Vue, options) {
    Vue.use(Loading.directive, Notification);
    Vue.prototype.$notify = Notification;
    Vue.prototype.$prompt = MessageBox.prompt;
    Vue.prototype.$confirm = MessageBox.confirm;
    Vue.prototype.$message = Message;
    coms.map((c) => {
      Vue.component(c.name, c);
    });
  }
};
