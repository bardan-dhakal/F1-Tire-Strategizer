import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Utility class for F1-style typography that matches the bold, impactful
/// font style seen in F1 digital interfaces
class F1Fonts {
  // Private constructor to prevent instantiation
  F1Fonts._();

  /// F1 Big Title - Large, bold, uppercase font for main titles
  /// Similar to "STORIES" title in F1 interface
  static TextStyle bigTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 36,
      fontWeight: FontWeight.w900,
      letterSpacing: -1.0,
      color: color ?? Colors.white,
      height: 1.0,
    );
  }

  /// F1 Section Title - Bold uppercase font for section headers
  /// Similar to card titles like "BEHIND THE SCENES", "QUALI", etc.
  static TextStyle sectionTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 24,
      fontWeight: FontWeight.w800,
      letterSpacing: -0.5,
      color: color ?? Colors.white,
      height: 1.1,
    );
  }

  /// F1 Card Title - Medium bold font for card titles
  static TextStyle cardTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 20,
      fontWeight: FontWeight.w800,
      letterSpacing: -0.3,
      color: color ?? Colors.white,
      height: 1.2,
    );
  }

  /// F1 Subtitle - Smaller bold font for subtitles
  /// Similar to "United States Grand Prix" text
  static TextStyle subtitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 14,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.2,
      color: color ?? Colors.white70,
      height: 1.3,
    );
  }

  /// F1 Label - Small uppercase font for labels
  /// Similar to "NEW" tags and other small labels
  static TextStyle label({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 11,
      fontWeight: FontWeight.w400,
      letterSpacing: 1.2,
      color: color ?? Colors.white,
      height: 1.0,
    );
  }

  /// F1 Data - Font for displaying data values
  static TextStyle data({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 16,
      fontWeight: FontWeight.w700,
      letterSpacing: 0.5,
      color: color ?? Colors.white,
      height: 1.2,
    );
  }

  /// F1 App Title - Special style for app title
  static TextStyle appTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 32,
      fontWeight: FontWeight.w900,
      letterSpacing: -0.8,
      color: color ?? const Color(0xFFE10600), // F1 Red
      height: 1.0,
    );
  }

  /// F1 Lap Title - Style for lap numbers and positions
  static TextStyle lapTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 18,
      fontWeight: FontWeight.w800,
      letterSpacing: -0.2,
      color: color ?? const Color(0xFFE10600),
      height: 1.1,
    );
  }

  /// F1 Position Title - Style for tyre positions (Front Left, etc.)
  static TextStyle positionTitle({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 20,
      fontWeight: FontWeight.w900,
      letterSpacing: -0.2,
      color: color ?? const Color(0xFFE10600),
      height: 1.0,
    );
  }

  /// F1 Body Text - Readable font for descriptions and longer text content
  static TextStyle bodyText({Color? color, double? fontSize}) {
    return GoogleFonts.inter(
      fontSize: fontSize ?? 14,
      fontWeight: FontWeight.w400,
      letterSpacing: 0.0,
      color: color ?? Colors.white70,
      height: 1.4,
    );
  }
}

/// Extension on TextStyle to easily apply F1 font styles
extension F1TextStyleExtension on TextStyle {
  /// Apply F1 big title style
  TextStyle get f1BigTitle => F1Fonts.bigTitle().merge(this);

  /// Apply F1 section title style
  TextStyle get f1SectionTitle => F1Fonts.sectionTitle().merge(this);

  /// Apply F1 card title style
  TextStyle get f1CardTitle => F1Fonts.cardTitle().merge(this);

  /// Apply F1 subtitle style
  TextStyle get f1Subtitle => F1Fonts.subtitle().merge(this);

  /// Apply F1 label style
  TextStyle get f1Label => F1Fonts.label().merge(this);

  /// Apply F1 data style
  TextStyle get f1Data => F1Fonts.data().merge(this);

  /// Apply F1 app title style
  TextStyle get f1AppTitle => F1Fonts.appTitle().merge(this);

  /// Apply F1 lap title style
  TextStyle get f1LapTitle => F1Fonts.lapTitle().merge(this);

  /// Apply F1 position title style
  TextStyle get f1PositionTitle => F1Fonts.positionTitle().merge(this);

  /// Apply F1 body text style
  TextStyle get f1BodyText => F1Fonts.bodyText().merge(this);
}
