import 'package:f1_analyzer/firebase_options.dart';
import 'package:f1_analyzer/start_page.dart';
import 'package:f1_analyzer/utils/f1_fonts.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

void main() async {
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PitPundits',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE10600), // F1 Red
          brightness: Brightness.dark,
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme)
            .copyWith(
              // F1-style headlines
              headlineLarge: F1Fonts.bigTitle(fontSize: 36),
              headlineMedium: F1Fonts.sectionTitle(fontSize: 28),
              headlineSmall: F1Fonts.cardTitle(fontSize: 24),

              // F1-style titles
              titleLarge: F1Fonts.cardTitle(fontSize: 22),
              titleMedium: F1Fonts.lapTitle(fontSize: 18),
              titleSmall: F1Fonts.data(fontSize: 16),

              // F1-style body text
              bodyLarge: GoogleFonts.inter(
                fontSize: 16,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.3,
                color: Colors.white,
              ),
              bodyMedium: GoogleFonts.inter(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.3,
                color: Colors.white70,
              ),
              bodySmall: GoogleFonts.inter(
                fontSize: 12,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.4,
                color: Colors.white60,
              ),

              // F1-style labels
              labelLarge: F1Fonts.label(fontSize: 14),
              labelMedium: F1Fonts.label(fontSize: 12),
              labelSmall: F1Fonts.label(fontSize: 11),
            ),
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          titleTextStyle: F1Fonts.appTitle(fontSize: 24),
        ),
        cardTheme: const CardThemeData(
          elevation: 0,
          shape: RoundedRectangleBorder(),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            elevation: 0,
            shape: const RoundedRectangleBorder(),
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          ),
        ),
      ),
      home: const StartPage(),
    );
  }
}
