const e = React.createElement;

// class LikeButton extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = { liked: false };
//   }
//
//   render() {
//     if (this.state.liked) {
//       return 'You liked this.';
//     }
//
//     return e(
//       'button',
//       { onClick: () => this.setState({ liked: true }) },
//       'Like'
//     );
//   }
// }

class Example extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

  }


  componentDidMount() {
    fetch('http://127.0.0.1:8000/admin/users/read/')
            .then(response => console.log(response.json()))
            .then(result => this.setState({data: result, isFetching: false }));
    // document.title = `Вы нажали ${this.state.count} раз`;

  }
  componentDidUpdate() {
    // document.title = `Вы нажали ${this.state.count} раз`;
  }



  render() {
    return (
      <div>
        123
        {this.state.data}
        {/*<button onClick={() => this.setState({ count: this.state.count + 1 })}>*/}
        {/*  Нажми на меня*/}
        {/*</button>*/}
      </div>
    );
  }
}

const domContainer = document.querySelector('#admin_main');
ReactDOM.render(e(Example), domContainer);