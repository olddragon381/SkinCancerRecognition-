import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(8),
      children: <Widget>[
        const Center(
            child: Text(
          'Trần Thanh Tùng - 2100009418',
        )),
        const Center(child: Text('Lê Trung An - 2100007880')),
        const Center(child: Text('La Thành Duy - 2100004752')),
        const Center(child: Text('	Huỳnh Việt Thành- 2100004924')),
        const Center(child: Text('Trần Lê Nhựt Trường - 2100008857')),
        const SizedBox(
          height: 8,
        ),
        ElevatedButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Go back!'),
        ),
      ],
    );
  }
}
