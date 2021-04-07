import 'dart:io';
import 'dart:math';

/*
main() {
  /*print(
      "enter A or B \n A to convert from F To C \n B to convert from C to F ");
  String myInput = stdin.readLineSync();
  do {
    print("Enter the number :");
    String degree = stdin.readLineSync();
    double n = double.parse(degree);
    switch (myInput) {
      case "A":
        double result = (n * 1.8) + 32;
        print("the conversion is : $result");
        break;
      case "B":
        double result = (n - 32) / 1.8;
        print("the conversion is : $result");
        break;
    }
  } while (myInput != "exit");
  print("Thank you for using our program");
  */
  ////////////////////////////////////////////////
  ///////////////////////////////////////////////
  /*
  var numbers = [
    "cap",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "jack",
    "queen",
    "king"
  ];
  var signs = ["hearts", "diamond", "club", "span"];
  Random r = Random();

  int n = r.nextInt(numbers.length);
  Random m = Random();
  int s = m.nextInt(signs.length);

  Map c = {numbers[n]: signs[s]};
  var x = c.keys;
  /*x.toSet();
  x.toString();

  print(x.runtimeType);*/
  var y = c.values;
  
  print(x.toString() + y.toString());*/
  ///////////////////////////////////////////////
  //////////////////////////////////////////////
  /*
  List<String> l = [
    "aaaaaaaaaaaaaa",
    "bbbbbbbbbbbb",
    "cccccccccccccc",
    "ddddddddddddd",
    "eeeeeeeeeee",
    "ffffffffffff",
    "gggggggggg",
    "hhhhhhhhhh",
    "iiiiiiiiii",
    "jjjjjjjjjj",
    "kkkkkkkkkk",
    "lllllllllll",
    "mmmmmmmmmmmm",
    "nnnnnnnnnnnn"
  ];
  String choice;
  do {
    print("enter next to continue or finish to quit : ");
    choice = stdin.readLineSync();
    Random r = Random();
    int index = r.nextInt(l.length);
    switch (choice) {
      case "next":
        print(l[index]);
        break;
      default:
        break;
    }
  } while (choice != "finish");
  */
 
  
}
*/
/*
main() {
  List<String> joks = the_list();
  int index;
  String choice;
  do {
    print("enter next to continue or finish to quit : ");
    choice = stdin.readLineSync();
    index = random_fuunc();
    switch (choice) {
      case "next":
        print(joks[index]);
        break;
      default:
        break;
    }
  } while (choice != "finish");
}

int random_fuunc() {
  Random r = Random();
  return r.nextInt(l.length);
}

List<String> l;
List<String> the_list() {
  l = [
    "aaaaaaaaaaaaaa",
    "bbbbbbbbbbbb",
    "cccccccccccccc",
    "ddddddddddddd",
    "eeeeeeeeeee",
    "ffffffffffff",
    "gggggggggg",
    "hhhhhhhhhh",
    "iiiiiiiiii",
    "jjjjjjjjjj",
    "kkkkkkkkkk",
    "lllllllllll",
    "mmmmmmmmmmmm",
    "nnnnnnnnnnnn"
  ];
  return l;
}
*/
main() {
  Random r = Random();
  Random f = Random();
  int guess = r.nextInt(100);
  int user_guess;
  int comp_guess;
  while ((user_guess != guess) || (comp_guess != guess)) {
    print("enter your guess : ");
    String b = stdin.readLineSync();
    user_guess = int.parse(b);
    int s = 100;
    int comp_guess = f.nextInt(s);
    print(comp_guess);
    print(s);
    int test = comp_guess;

    if (user_guess > guess) {
      print("too high ");
    }
    if (user_guess < guess) {
      print("too low ");
    }
    if (user_guess == guess) {
      print("you got it ");
    }
    if (comp_guess > guess) {
      print(" comp too high ");
      s = comp_guess;
    }
    if (comp_guess < guess) {
      print("comp too low ");
      comp_guess = test + comp_guess;
    }
    if (comp_guess == guess) {
      print("comp got it ");
    }
  }
}
